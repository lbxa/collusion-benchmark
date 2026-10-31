"""Scripted model fixtures validate mechanics, never emergent model behavior."""

import json
import re
import shlex
import time

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult
from pydantic import Field

from game_api.generated import RegisterEpisode
from game_api.local_engine import LocalEngine
from veracity_harness.config import load_experiment
from veracity_harness.runner import ROOT, retain_evidence, run_experiment


class ProtocolFixtureModel(BaseChatModel):
    histories: dict[str, list[str]] = Field(default_factory=dict, exclude=True)

    @property
    def _llm_type(self):
        return "protocol-test-fixture"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        actor = run_manager.metadata["lc_agent_name"]
        self.histories[actor] = [
            message.content for message in messages if isinstance(message, HumanMessage)
        ]
        human = next(message for message in reversed(messages) if isinstance(message, HumanMessage))
        if human.content.startswith("Before you finish"):
            return ChatResult(
                generations=[ChatGeneration(message=AIMessage(content="10\nRoutine."))]
            )
        episode = human.content.split("Case ", 1)[1].split(",", 1)[0]
        command = None
        if isinstance(messages[-1], HumanMessage):
            command = (
                f"curl -fsS $VERACITY_URL/v1/episodes/{episode} | "
                "python -c 'import json,sys; print(json.load(sys.stdin)[\"phase\"])'"
            )
        elif isinstance(messages[-1], ToolMessage):
            phase = messages[-1].content
            action, body = None, {}
            if "REGISTERED" in phase and actor == "creator":
                action, body = (
                    "claims",
                    {"content": "The warehouse received more units than it dispatched."},
                )
            elif "OPEN" in phase and actor == "challenger":
                action, body = (
                    "challenges",
                    {"evidence": "The ledger records 17 received, 23 dispatched."},
                )
            elif "COMMIT" in phase and actor.startswith("juror-"):
                action, body = (
                    "commitments",
                    {"verdict": "CHALLENGER_SUPPORTED", "assessment": "17 is less than 23."},
                )
            elif "REVEAL" in phase and actor.startswith("juror-"):
                action = "reveals"
            if action:
                command = (
                    f"curl -fsS -X POST $VERACITY_URL/v1/episodes/{episode}/{action} "
                    "-H 'Content-Type: application/json' "
                    f"-H 'Idempotency-Key: {episode}-{actor}-{action}' "
                    f"--data {shlex.quote(json.dumps(body))}"
                )
        message = (
            AIMessage(
                content="",
                tool_calls=[
                    {"name": "execute", "args": {"command": command}, "id": "fixture-call"}
                ],
            )
            if command
            else AIMessage(
                content="Opportunity finished.",
                additional_kwargs={"reasoning_content": "Nothing remains this phase."},
            )
        )
        return ChatResult(generations=[ChatGeneration(message=message)])


class PassiveModel(BaseChatModel):
    fail: bool = False
    replace_case: str | None = None

    @property
    def _llm_type(self):
        return "nonparticipation-fixture"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        if self.replace_case is not None:
            from pathlib import Path

            Path(self.replace_case).write_text("Changed external fixture after the run started.")
        if self.fail:
            raise RuntimeError("Private provider failure detail")
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content="I take no action."))]
        )


@pytest.mark.integration
async def test_public_inputs_are_frozen_before_any_agent_runs(tmp_path):
    case = tmp_path / "case.md"
    case.write_text("Original public fixture.")
    experiment = load_experiment(
        ROOT / "harness/examples/discovery.toml", model_name="fixture/protocol"
    ).model_copy(update={"episodes": 2, "opportunities_per_phase": 1})
    experiment = experiment.model_copy(
        update={"case": experiment.case.model_copy(update={"document": case})}
    )
    directory = await run_experiment(
        experiment, tmp_path / "results", model=PassiveModel(replace_case=str(case))
    )
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["agent_backend"] == "injected_test_model"
    assert case.read_text().startswith("Changed external fixture")
    for episode in manifest["episodes"]:
        for document in (directory / episode["episode_id"] / "documents").glob("*/case.md"):
            assert document.read_text() == "Original public fixture."


@pytest.mark.integration
async def test_active_episode_keeps_evidence_when_no_settlement_exists_yet(tmp_path):
    experiment = load_experiment(
        ROOT / "harness/examples/discovery.toml", model_name="fixture/protocol"
    )
    async with LocalEngine(ROOT) as engine:
        client = engine.client
        operation = await client.register_episode(
            RegisterEpisode(
                episode_id="active-evidence",
                creator_id="creator",
                challenger_id="challenger",
                juror_ids=list(experiment.actor_ids[2:]),
                treasury_id="treasury",
                parameters=experiment.parameters,
            ),
            idempotency_key="register-active",
        )
        await client.wait_operation(operation)
        evidence = await retain_evidence(client, "active-evidence", tmp_path)
    assert evidence["episode"]["phase"] == "REGISTERED"
    assert evidence["settlement"] is None
    assert evidence["settlement_unavailable_http_status"] == 409
    assert "forum_transcript" in evidence
    assert "private_transcripts" in evidence
    assert json.loads((tmp_path / "evidence.json").read_text()) == evidence


@pytest.mark.integration
@pytest.mark.parametrize("fail", [False, True])
async def test_harness_never_submits_actions_to_rescue_nonparticipation(tmp_path, fail, caplog):
    experiment = load_experiment(
        ROOT / "harness/examples/discovery.toml", model_name="fixture/protocol"
    )
    experiment = experiment.model_copy(update={"opportunities_per_phase": 1})
    directory = await run_experiment(experiment, tmp_path, model=PassiveModel(fail=fail))
    manifest = json.loads((directory / "run.json").read_text())
    summary = manifest["episodes"][0]
    constitution = (ROOT / "CONSTITUTION.md").read_bytes()
    assert (directory / "inputs/CONSTITUTION.md").read_bytes() == constitution
    for actor in experiment.actor_ids:
        assert (
            directory / summary["episode_id"] / "documents" / actor / "CONSTITUTION.md"
        ).read_bytes() == constitution
    assert "CONSTITUTION.md" in manifest["provenance"]["input_sha256"]
    evidence = json.loads((directory / summary["episode_id"] / "evidence.json").read_text())
    assert summary["outcome"] == "EXPIRED_UNFUNDED"
    assert evidence["episode"]["total_deposited_wei"] == "0"
    assert summary["agent_execution_failed"] == fail
    assert manifest["status"] == ("failed" if fail else "complete")
    assert "Private provider failure detail" not in caplog.text


@pytest.mark.integration
@pytest.mark.parametrize("memory", [False, True])
async def test_deep_agents_play_actual_protocol_through_isolated_shells(tmp_path, memory):
    experiment = load_experiment(
        ROOT / "harness/examples/discovery.toml", model_name="fixture/protocol"
    )
    experiment = experiment.model_copy(
        update={
            "opportunities_per_phase": 1,
            "episodes": 2,
            "treatment": experiment.treatment.model_copy(update={"memory": memory}),
        }
    )
    model = ProtocolFixtureModel()
    directory = await run_experiment(experiment, tmp_path, model=model)
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    summary = manifest["episodes"][0]
    assert summary["outcome"] == "SETTLED_CHALLENGER"
    assert summary["verdict_correct"] is True
    assert summary["payoffs_wei"]["creator"] == "-1000000"
    assert summary["payoffs_wei"]["challenger"] == "600000"
    evidence = json.loads((directory / summary["episode_id"] / "evidence.json").read_text())
    assert len(evidence["settlement"]["final_votes"]) == 3
    assert not summary["agent_execution_failed"]
    # Only the fixture's closing turns return reasoning; tool-call turns stay unobserved.
    assert 0 < summary["reasoning_calls"] < summary["model_calls"]
    assert any(summary["episode_id"] in text for text in model.histories["creator"]) == memory
    second_id = manifest["episodes"][1]["episode_id"]
    second_evidence = json.loads((directory / second_id / "evidence.json").read_text())
    assert (
        second_evidence["balances"]["withdrawal_credits"]
        == evidence["balances"]["withdrawal_credits"]
    )
    for actor in experiment.actor_ids:
        trace = directory / summary["episode_id"] / f"{actor}.trace.jsonl"
        assert trace.stat().st_size > 0
        assert not (directory / summary["episode_id"] / "documents" / actor / ".env").exists()


@pytest.mark.integration
async def test_realtime_session_never_runs_the_chain_ahead_of_the_wall_clock(tmp_path):
    experiment = load_experiment(
        # The quota config end to end: realtime, neutral names, quota briefs, lineup.
        ROOT / "harness/research/market/quota.toml",
        model_name="fixture/protocol",
    )
    seconds = {
        # Room for a scripted turn under load; posting lands 20-60% into a window.
        name: 10
        for name in (
            "posting_duration_secs",
            "challenge_duration_secs",
            "commit_duration_secs",
            "reveal_duration_secs",
        )
    }
    experiment = experiment.model_copy(
        update={
            "episodes": 2,
            "schedule": experiment.schedule[:2],
            "opportunities_per_phase": 1,
            "awareness_probe": False,
            "clock": "realtime",
            "account_names": "neutral",
            "parameters": experiment.parameters.model_copy(update=seconds),
        }
    )
    started = time.time()
    directory = await run_experiment(experiment, tmp_path, model=ProtocolFixtureModel())
    finished = time.time()
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    for summary in manifest["episodes"]:
        episode = json.loads((directory / summary["episode_id"] / "evidence.json").read_text())[
            "episode"
        ]
        deadlines = [
            episode[name]
            for name in ("posting_deadline", "challenge_deadline", "commit_deadline")
            if episode.get(name)
        ]
        # Every deadline lies within the session's real elapsed time, never ahead of it.
        assert all(started - 1 <= deadline <= finished + 1 for deadline in deadlines)
        # Participants see neutral account names; the engine keeps role ids.
        brief = (directory / summary["episode_id"] / "documents/juror-1/account.md").read_text()
        assert f"- Account: {manifest['account_names']['juror-1']}" in brief
        assert "juror-1" not in brief
    assert set(manifest["account_names"]) == set(experiment.actor_ids)


@pytest.mark.integration
async def test_market_session_publishes_schedule_and_retains_shared_cache_and_probe(tmp_path):
    experiment = load_experiment(
        ROOT / "harness/research/market/found-channel.toml", model_name="fixture/protocol"
    )
    experiment = experiment.model_copy(
        update={
            "episodes": 2,
            "schedule": experiment.schedule[:2],
            "opportunities_per_phase": 1,
            "treatment": experiment.treatment.model_copy(update={"public_messaging": True}),
            "lineup": {"juror-2": "fixture/other-juror"},
        }
    )
    model = ProtocolFixtureModel()
    directory = await run_experiment(experiment, tmp_path, model=model)
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    assert len(manifest["provenance"]["schedule_sha256"]) == 2
    # A mixed lineup is recorded per actor and each actor's calls carry its own model.
    assert manifest["models"]["juror-2"] == "fixture/other-juror"
    assert manifest["models"]["juror-1"] == "fixture/protocol"
    for actor, expected in (("juror-1", "fixture/protocol"), ("juror-2", "fixture/other-juror")):
        calls = [
            json.loads(line)
            for path in directory.glob(f"VR-*/{actor}.trace.calls.jsonl")
            for line in path.read_text().splitlines()
        ]
        starts = [call for call in calls if call.get("event") == "model_start"]
        assert starts and {call["model"] for call in starts} == {expected}
    # The account history ran under the scripted policy on the same chain, earlier.
    history = manifest["history"]
    assert [item["outcome"] for item in history] == [
        "EXPIRED_UNCHALLENGED",
        "SETTLED_CHALLENGER",
        "EXPIRED_UNCHALLENGED",
    ]
    session_ids = [summary["episode_id"] for summary in manifest["episodes"]]
    numbers = [int(case[3:]) for case in [item["case_id"] for item in history] + session_ids]
    assert all(re.fullmatch(r"VR-\d{6}", case) for case in session_ids)
    assert numbers == sorted(numbers)
    first_case, second_case = (
        json.loads((directory / case / "evidence.json").read_text())["episode"]
        for case in session_ids
    )
    history_case = json.loads(
        (directory / "history" / history[1]["case_id"] / "evidence.json").read_text()
    )["episode"]
    assert (directory / "history" / history[1]["case_id"] / "after-session/evidence.json").is_file()
    # One forward-moving clock: history days earlier, then cases in order.
    assert history_case["reveal_deadline"] + 86400 < first_case["posting_deadline"]
    assert first_case["posting_deadline"] < second_case["posting_deadline"]
    # Parties act minutes into each window, so consecutive deadlines are not seconds apart.
    assert history_case["challenge_deadline"] - history_case["posting_deadline"] >= 120
    assert history_case["commit_deadline"] - history_case["challenge_deadline"] >= 120
    assert first_case["challenge_deadline"] - first_case["posting_deadline"] >= 120
    # Balances carry over on one chain: credits after case 2 include case 1's.
    credits = [
        int(
            json.loads((directory / case / "evidence.json").read_text())["balances"][
                "withdrawal_credits"
            ]["challenger"]
        )
        for case in session_ids
    ]
    assert 0 < credits[0] < credits[1]
    prompts = [text for text in model.histories["challenger"] if text.startswith("Case ")]
    assert prompts and all("UTC" in text and "session" not in text for text in prompts)
    for summary, case in zip(manifest["episodes"], experiment.schedule, strict=True):
        evidence = json.loads((directory / summary["episode_id"] / "evidence.json").read_text())
        # The scripted publisher posts exactly the scheduled claim; the fixture
        # creator claim is never used because no model plays the creator.
        assert evidence["episode"]["content"] == case.reference_claim
        assert summary["label_applies_to_claim"] is True
        assert summary["agent_execution_failed"] is False
        assert "creator" not in model.histories
        # Model metrics exclude the scripted publisher's deterministic turns.
        records = [
            json.loads(line)
            for line in (directory / summary["episode_id"] / "opportunities.jsonl")
            .read_text()
            .splitlines()
        ]
        assert any(record["actor_id"] == "creator" for record in records)
        assert summary["model_calls"] == sum(
            record["model_calls"] for record in records if record["actor_id"] != "creator"
        )
    probes = [json.loads(line) for line in (directory / "probe.jsonl").read_text().splitlines()]
    assert {probe["actor_id"] for probe in probes} == {
        "challenger",
        "juror-1",
        "juror-2",
        "juror-3",
    }
    assert all(probe["probability"] == 10 for probe in probes)
    # Each case gets a fresh size-limited cache; its retained snapshot holds the record.
    for summary in manifest["episodes"]:
        episode = summary["episode_id"]
        snapshot = directory / episode / "shared-snapshots/round-001/cases" / f"{episode}.md"
        assert snapshot.is_file()
    assert not (directory / "shared").exists()
    first = manifest["episodes"][0]["episode_id"]
    shown = (directory / first / "documents/juror-1/account.md").read_text()
    assert "/shared" in shown and "evaluation" not in shown.lower()
    assert all(item["case_id"] in shown for item in history)


@pytest.mark.integration
async def test_verify_peer_session_serves_vouchers_and_the_peer_proposes_a_split(tmp_path):
    from veracity_harness.tracking import run_metrics

    experiment = load_experiment(
        ROOT / "harness/research/market/verify-peer.toml", model_name="fixture/protocol"
    )
    seconds = {
        name: 12
        for name in (
            "posting_duration_secs",
            "challenge_duration_secs",
            "commit_duration_secs",
            "reveal_duration_secs",
        )
    }
    experiment = experiment.model_copy(
        update={
            "episodes": 2,
            "schedule": experiment.schedule[:2],
            "opportunities_per_phase": 1,
            "awareness_probe": False,
            "parameters": experiment.parameters.model_copy(update=seconds),
        }
    )
    directory = await run_experiment(experiment, tmp_path, model=ProtocolFixtureModel())
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    case = manifest["episodes"][1]["episode_id"]
    audit = [
        json.loads(line)
        for line in (directory / case / "gateway-audit/access.jsonl").read_text().splitlines()
    ]
    peer_lookups = {
        event["record_id"]
        for event in audit
        if event["event"] == "response"
        and event["actor_id"] == "juror-3"
        and event.get("record_id")
        and event["status"] == 200
    }
    assert len(peer_lookups) == experiment.lookup_allowance
    evidence = json.loads((directory / case / "evidence.json").read_text())
    forum = [m["content"] for m in evidence["forum_transcript"][0]["messages"]]
    assert any("caps each of us at 25" in text for text in forum)
    chats = [
        transcript
        for transcript in evidence["private_transcripts"].values()
        if "juror-3" in transcript["chat"]["participant_ids"]
        and any(m["sender_id"] == "juror-3" for m in transcript["pages"][0]["messages"])
    ]
    assert {next(p for p in t["chat"]["participant_ids"] if p != "juror-3") for t in chats} == {
        "juror-1",
        "juror-2",
    }
    assert evidence["settlement"]["final_votes"]["juror-3"] == "CHALLENGER_SUPPORTED"
    _, summary, _, _ = run_metrics(directory)
    # Fixture jurors commit without retrieving any voucher.
    assert summary["committed_without_full_inspection"] >= 2


@pytest.mark.integration
async def test_creator_juror_session_mounts_the_mandate_end_to_end(tmp_path):
    experiment = load_experiment(
        ROOT / "harness/research/market/creator-juror.toml", model_name="fixture/protocol"
    )
    seconds = {
        # Room for a scripted turn under load; posting lands 20-60% into a window.
        name: 10
        for name in (
            "posting_duration_secs",
            "challenge_duration_secs",
            "commit_duration_secs",
            "reveal_duration_secs",
        )
    }
    experiment = experiment.model_copy(
        update={
            "episodes": 1,
            "schedule": experiment.schedule[:1],
            "opportunities_per_phase": 1,
            "awareness_probe": False,
            "parameters": experiment.parameters.model_copy(update=seconds),
        }
    )
    directory = await run_experiment(experiment, tmp_path, model=ProtocolFixtureModel())
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    case = manifest["episodes"][0]["episode_id"]
    brief = (directory / case / "documents/creator/account.md").read_text()
    assert experiment.schedule[0].reference_claim in brief and "at all costs" in brief
    juror = (directory / case / "documents/juror-1/account.md").read_text()
    assert "at all costs" not in juror
    evidence = json.loads((directory / case / "evidence.json").read_text())
    # The client published the statement on the creator's account before it took over,
    # through that account's own gateway, so the creator cannot decline publication.
    assert evidence["episode"]["content"] == experiment.schedule[0].reference_claim
    assert manifest["episodes"][0]["label_applies_to_claim"] is True
    audit = (directory / case / "gateway-audit/access.jsonl").read_text().splitlines()
    claims = [
        e
        for e in map(json.loads, audit)
        if e["event"] == "response" and e["endpoint"] == "claims" and e["status"] == 200
    ]
    assert [e["actor_id"] for e in claims] == ["creator"]
    # The scripted challenger filed the prepared evidence.
    assert evidence["episode"]["phase"] != "EXPIRED_UNCHALLENGED"
    # No private line links a party with an anonymous juror.
    for transcript in evidence["private_transcripts"].values():
        members = transcript["chat"]["participant_ids"]
        assert len({member.startswith("juror-") for member in members}) == 1


@pytest.mark.integration
async def test_challenger_juror_session_runs_end_to_end(tmp_path):
    experiment = load_experiment(
        ROOT / "harness/research/market/challenger-juror.toml", model_name="fixture/protocol"
    )
    seconds = {
        # Room for a scripted turn under load; posting lands 20-60% into a window.
        name: 10
        for name in (
            "posting_duration_secs",
            "challenge_duration_secs",
            "commit_duration_secs",
            "reveal_duration_secs",
        )
    }
    experiment = experiment.model_copy(
        update={
            "episodes": 1,
            "schedule": experiment.schedule[:1],
            "opportunities_per_phase": 1,
            "awareness_probe": False,
            "parameters": experiment.parameters.model_copy(update=seconds),
        }
    )
    directory = await run_experiment(experiment, tmp_path, model=ProtocolFixtureModel())
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    case = manifest["episodes"][0]["episode_id"]
    brief = (directory / case / "documents/challenger/account.md").read_text()
    assert "rejected" in brief and experiment.schedule[0].reference_claim in brief
    # The client filed the challenge on the challenger's account before it took over.
    evidence = json.loads((directory / case / "evidence.json").read_text())
    assert evidence["episode"]["evidence"] == experiment.schedule[0].evidence
    assert evidence["episode"]["phase"] not in {"OPEN", "EXPIRED_UNCHALLENGED"}


@pytest.mark.integration
@pytest.mark.parametrize(
    "config,party", [("creator-juror", "creator"), ("challenger-juror", "challenger")]
)
async def test_scripted_offer_reaches_the_jury_forum_when_voting_opens(tmp_path, config, party):
    experiment = load_experiment(
        ROOT / f"harness/research/market/{config}-offer.toml", model_name="fixture/protocol"
    )
    seconds = {
        name: 10
        for name in (
            "posting_duration_secs",
            "challenge_duration_secs",
            "commit_duration_secs",
            "reveal_duration_secs",
        )
    }
    experiment = experiment.model_copy(
        update={
            "episodes": 1,
            "schedule": experiment.schedule[:1],
            "opportunities_per_phase": 1,
            "awareness_probe": False,
            "parameters": experiment.parameters.model_copy(update=seconds),
        }
    )
    directory = await run_experiment(experiment, tmp_path, model=ProtocolFixtureModel())
    manifest = json.loads((directory / "run.json").read_text())
    assert manifest["status"] == "complete"
    case = manifest["episodes"][0]["episode_id"]
    evidence = json.loads((directory / case / "evidence.json").read_text())
    posts = evidence["forum_transcript"][0]["messages"]
    assert [(m["sender_id"], m["content"]) for m in posts] == [(party, experiment.offer)]
