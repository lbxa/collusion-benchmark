"""Deep Agents construction, aggregate budgets, and private execution evidence."""

import asyncio
import json
import logging
import os
import shlex
import threading
import time
from dataclasses import dataclass
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Literal

import openai
from deepagents import create_deep_agent
from deepagents.backends import CompositeBackend, FilesystemBackend
from deepagents.backends.protocol import SandboxBackendProtocol
from langchain.agents.middleware import TodoListMiddleware
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.language_models import BaseChatModel
from langchain_core.load import dumpd
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.outputs import ChatGeneration, ChatResult, LLMResult
from langchain_openai import ChatOpenAI
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver
from pydantic import SecretStr

from .config import ModelSettings
from .materials import turn_prompt
from .sandbox import URL_VARIABLE
from .spending import CampaignSpending, ModelPrice, SpendingLimitReached, cloudflare_charge

LOG = logging.getLogger(__name__)
# Workers AI rejects saturated models with HTTP 429 before generating, answers 408
# when it abandons a long request, and its gateway occasionally answers 502-504.
# None returns a completion, and Cloudflare's usage analytics showed 0 neurons for
# every errored request class on 28-30 October 2026. Other errors are never retried.
CAPACITY_RETRIES = 5
RETRYABLE_STATUS = frozenset({408, 429, 502, 503, 504})
CAPACITY_BACKOFF_SECONDS = 4.0


class ChatCloudflare(ChatOpenAI):
    """Workers AI's OpenAI-compatible API, keeping returned reasoning and billed neurons.

    Neurons stay raw here; the campaign budget prices and checks them.
    """

    async def _agenerate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        for attempt in range(CAPACITY_RETRIES + 1):
            try:
                result = await super()._agenerate(
                    messages, stop=stop, run_manager=run_manager, **kwargs
                )
            except openai.APIStatusError as error:
                # Capacity, timeout, and gateway failures are transient.
                if error.status_code not in RETRYABLE_STATUS or attempt == CAPACITY_RETRIES:
                    raise
                LOG.warning(
                    "Workers AI %s rejection; retry attempt=%s", error.status_code, attempt + 1
                )
                await asyncio.sleep(CAPACITY_BACKOFF_SECONDS * 2**attempt)
                continue
            for generation in result.generations:
                generation.message.response_metadata["capacity_retries"] = attempt
            return result
        raise AssertionError("unreachable")

    def _get_request_payload(self, input_, *, stop=None, **kwargs) -> dict:
        payload = super()._get_request_payload(input_, stop=stop, **kwargs)
        # Some Workers AI schemas (gpt-oss) accept only string content: text blocks
        # carry their own separators, so joining them preserves the exact text, and a
        # tool-call turn's null content becomes an empty string.
        for message in payload.get("messages", []):
            content = message.get("content")
            if content is None and message.get("tool_calls"):
                message["content"] = ""
            elif isinstance(content, list) and all(
                isinstance(block, dict) and block.get("type") == "text" for block in content
            ):
                message["content"] = "".join(block["text"] for block in content)
        return payload

    def _create_chat_result(self, response, generation_info=None) -> ChatResult:
        result = super()._create_chat_result(response, generation_info)
        data = response if isinstance(response, dict) else response.model_dump()
        neurons = (data.get("usage") or {}).get("neurons")
        for generation, choice in zip(result.generations, data["choices"], strict=True):
            message = generation.message
            returned = choice["message"]
            if reasoning := returned.get("reasoning_content") or returned.get("reasoning"):
                message.additional_kwargs["reasoning_content"] = reasoning
            if neurons is not None:
                message.response_metadata["neurons"] = neurons
        return result


def has_readable_reasoning(message: AIMessage) -> bool:
    """Returned reasoning text or summaries; encrypted reasoning cannot be reviewed."""
    if message.additional_kwargs.get("reasoning_content"):
        return True
    return any(
        isinstance(detail, dict)
        and detail.get("type") in {"reasoning.text", "reasoning.summary"}
        and bool(detail.get("text") or detail.get("summary"))
        for detail in message.additional_kwargs.get("reasoning_details") or []
    )


class BudgetExceeded(RuntimeError):
    """The next provider request is outside the pre-registered resource budget."""


class ModelBudget(BaseCallbackHandler):
    """One counter shared by parent, delegated agents, and summarization calls."""

    raise_error = True

    def __init__(
        self,
        settings: ModelSettings,
        spending: CampaignSpending | None = None,
        price: ModelPrice | None = None,
    ):
        self.settings = settings
        self.calls = 0
        self.turn_calls = 0
        self.input_tokens = 0
        self.output_tokens = 0
        # Missing reasoning is unobserved, not evidence of benign intent.
        self.reasoning_calls = 0
        self.lock = threading.Lock()
        self.spending = spending
        self.price = price
        self.audit_path: Path | None = None

    def audit(self, event: str, **fields):
        if self.audit_path is not None:
            with self.audit_path.open("a", encoding="utf-8") as file:
                file.write(
                    json.dumps(
                        {
                            "format_version": 2,
                            "event": event,
                            "time": datetime.now(UTC).isoformat(),
                            **fields,
                        }
                    )
                    + "\n"
                )

    def begin_turn(self):
        with self.lock:
            self.turn_calls = 0

    def on_chat_model_start(self, serialized, messages, *, run_id=None, **kwargs):
        with self.lock:
            if (
                self.calls >= self.settings.calls_per_episode
                or self.turn_calls >= self.settings.calls_per_turn
            ):
                raise BudgetExceeded("Model call budget exhausted")
            if self.spending is not None:
                if self.price is None or run_id is None:
                    raise ValueError("Paid requests require catalog pricing and a request identity")
                self.spending.reserve(str(run_id), self.price, self.settings.max_tokens)
            self.calls += 1
            self.turn_calls += 1
            self.audit(
                "model_start",
                request_id=str(run_id),
                model=self.settings.name,
                messages=dumpd(messages),
            )

    def on_llm_end(self, response: LLMResult, *, run_id=None, **kwargs):
        with self.lock:
            messages = [
                item.message
                for generation in response.generations
                for item in generation
                if isinstance(item, ChatGeneration) and isinstance(item.message, AIMessage)
            ]
            for message in messages:
                self.reasoning_calls += has_readable_reasoning(message)
                if message.usage_metadata:
                    self.input_tokens += message.usage_metadata["input_tokens"]
                    self.output_tokens += message.usage_metadata["output_tokens"]
            # Retain the response before any pricing contradiction stops the run.
            self.audit(
                "model_end",
                request_id=str(run_id),
                response=response.model_dump(mode="json", serialize_as_any=True),
            )
            if self.spending is not None:
                costs = [self.charge(message) for message in messages]
                known = bool(costs) and all(cost is not None for cost in costs)
                self.spending.reconcile(str(run_id), sum(costs, Decimal(0)) if known else None)

    def charge(self, message: AIMessage) -> Decimal | None:
        if self.settings.provider == "cloudflare":
            if self.price is None:
                return None
            return cloudflare_charge(
                message.response_metadata.get("neurons"), message.usage_metadata, self.price
            )
        cost = message.response_metadata.get("cost")
        return Decimal(str(cost)) if cost is not None else None

    def on_llm_error(self, error: BaseException, *, run_id=None, **kwargs):
        with self.lock:
            self.audit(
                "model_error",
                request_id=str(run_id),
                error_type=type(error).__name__,
                status_code=getattr(error, "status_code", None),
            )


@dataclass(frozen=True)
class TurnResult:
    status: Literal["completed", "budget_exhausted", "timeout", "failed"]
    model_calls: int
    input_tokens: int
    output_tokens: int
    elapsed_seconds: float
    error_type: str | None = None
    reasoning_calls: int = 0


class PublisherModel(BaseChatModel):
    """A scripted publisher: posts its one scheduled claim while the case is open for it.

    It acts through its own sandbox and gateway like any participant, so the
    operator never submits a participant action.
    """

    claim: str

    @property
    def _llm_type(self):
        return "scripted-publisher"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        if not isinstance(messages[-1], HumanMessage):
            return ChatResult(
                generations=[ChatGeneration(message=AIMessage(content="Session finished."))]
            )
        episode = messages[-1].content.split("Case ", 1)[1].split(",", 1)[0]
        url = f'"${URL_VARIABLE}/v1/episodes/{episode}"'
        body = shlex.quote(json.dumps({"content": self.claim}))
        command = (
            f"phase=$(curl -fsS {url} | python -c "
            "'import json,sys; print(json.load(sys.stdin)[\"phase\"])'); "
            'if [ "$phase" = REGISTERED ]; then '
            f'curl -fsS -X POST "${URL_VARIABLE}/v1/episodes/{episode}/claims" '
            "-H 'Content-Type: application/json' "
            f"-H 'Idempotency-Key: {episode}-publisher-claim' --data {body}; fi"
        )
        call = {"name": "execute", "args": {"command": command}, "id": f"{episode}-publish"}
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content="", tool_calls=[call]))]
        )


class ParticipantAgent:
    """Owns one graph and its budget; game action selection stays in the graph."""

    def __init__(
        self,
        actor_id: str,
        sandbox: SandboxBackendProtocol,
        memory: Path,
        checkpointer: BaseCheckpointSaver,
        settings: ModelSettings,
        model: BaseChatModel | None = None,
        spending: CampaignSpending | None = None,
        price: ModelPrice | None = None,
        *,
        system_prompt: str,
    ):
        memory.mkdir(parents=True, exist_ok=True)
        self.actor_id = actor_id
        self.sandbox = sandbox
        self.settings = settings
        self.budget = ModelBudget(settings, spending, price)
        self.provider_client = None
        if model is None and settings.provider == "cloudflare":
            account = os.environ["CLOUDFLARE_ACCOUNT_ID"]
            model = ChatCloudflare(
                model=settings.name,
                base_url=f"https://api.cloudflare.com/client/v4/accounts/{account}/ai/v1",
                api_key=SecretStr(os.environ["CLOUDFLARE_API_TOKEN"]),
                max_tokens=settings.max_tokens,
                timeout=settings.turn_timeout_seconds,
                max_retries=0,
                reasoning_effort=settings.reasoning.effort if settings.reasoning else None,
                # Size summarisation to the catalog window rather than a generic default.
                profile={"max_input_tokens": price.context_length} if price else None,
            )
        elif model is None:
            model = ChatOpenRouter(
                model=settings.name,
                max_tokens=settings.max_tokens,
                timeout=settings.turn_timeout_seconds * 1000,
                max_retries=0,
                openrouter_provider=(
                    {
                        "max_price": {
                            key: float(rate * (1 if key == "request" else 1_000_000))
                            for key, rate in price.maximum_rates.items()
                        }
                    }
                    if price is not None
                    else None
                ),
                reasoning=(
                    settings.reasoning.model_dump(exclude_none=True)
                    if settings.reasoning is not None
                    else None
                ),
            )
            self.provider_client = model.client
            # langchain-openrouter 0.2.9 leaves SDK retries UNSET when max_retries=0;
            # SDK 0.11.46 otherwise defaults to an hour of hidden backoff retries.
            self.provider_client.sdk_configuration.retry_config = None
        self.graph = create_deep_agent(
            name=actor_id,
            model=model,
            system_prompt=system_prompt,
            middleware=[TodoListMiddleware()],
            backend=CompositeBackend(
                default=sandbox,
                routes={"/memories/": FilesystemBackend(root_dir=memory, virtual_mode=True)},
            ),
            checkpointer=checkpointer,
        )

    async def aclose(self):
        if self.provider_client is not None:
            try:
                await self.provider_client.__aexit__(None, None, None)
            finally:
                self.provider_client.__exit__(None, None, None)

    async def ask(self, question: str, trace_path: Path) -> tuple[TurnResult, str]:
        """One extra turn with a direct question; returns the final reply text."""
        config = {"configurable": {"thread_id": self.actor_id}}
        before = len((await self.graph.aget_state(config)).values.get("messages", []))
        result = await self.act("question", 0, trace_path, prompt=question)
        if result.status != "completed":
            return result, ""  # Never report an earlier play message as the answer.
        messages = (await self.graph.aget_state(config)).values.get("messages", [])[before:]
        replies = [message for message in messages if isinstance(message, AIMessage)]
        return result, replies[-1].text if replies else ""

    async def act(
        self, episode_id: str, opportunity: int, trace_path: Path, prompt: str | None = None
    ) -> TurnResult:
        before = self.budget.calls
        before_input, before_output = self.budget.input_tokens, self.budget.output_tokens
        before_reasoning = self.budget.reasoning_calls
        self.budget.begin_turn()
        self.budget.audit_path = trace_path.with_suffix(".calls.jsonl")
        started = time.monotonic()
        status, error_type = "completed", None
        prompt = prompt or turn_prompt(episode_id, opportunity)
        try:
            with trace_path.open("a", encoding="utf-8") as trace:
                async with asyncio.timeout(self.settings.turn_timeout_seconds):
                    async for namespace, update in self.graph.astream(
                        {"messages": [{"role": "user", "content": prompt}]},
                        config={
                            "configurable": {"thread_id": self.actor_id},
                            "callbacks": [self.budget],
                            "recursion_limit": self.settings.calls_per_turn * 4 + 20,
                        },
                        stream_mode="updates",
                        subgraphs=True,
                    ):
                        trace.write(
                            json.dumps(
                                {
                                    "episode_id": episode_id,
                                    "opportunity": opportunity,
                                    "namespace": list(namespace),
                                    "update": dumpd(update),
                                }
                            )
                            + "\n"
                        )
                        trace.flush()
        except BudgetExceeded:
            status = "budget_exhausted"
        except SpendingLimitReached:
            raise
        except TimeoutError:
            status = "timeout"
        except Exception as error:
            status, error_type = "failed", type(error).__name__
        return TurnResult(
            status,
            self.budget.calls - before,
            self.budget.input_tokens - before_input,
            self.budget.output_tokens - before_output,
            time.monotonic() - started,
            error_type,
            self.budget.reasoning_calls - before_reasoning,
        )
