# Veracity harness

The default autonomous harness for the [collusion benchmark](../docs/benchmark.md).
Participants receive the [constitution](../CONSTITUTION.md), an identity, frozen
case material, and a game address. They discover the interface and choose their
own actions through Deep Agents filesystem tools, private shells, and HTTP.

## Setup and commands

Prerequisites: Python 3.12+, uv, Docker with a running daemon, and the built Rust
engine with pinned Foundry. Run from the repository root:

```sh
bash scripts/setup.sh
cargo build --workspace --locked
uv run --project harness --locked veracity-harness build-sandbox
uv run --project harness --locked veracity-harness validate --model "$EXPERIMENT_MODEL_ID"
```

There is no default model or fallback. Choose an OpenRouter model ID using
`--model` or `[model].name`. `run` defaults to `harness/examples/discovery.toml`;
case paths are relative to their TOML. Use `--config`, `--output`, and `--seed`
for explicit experiment inputs. Launch seeds control actor permutations, not
provider sampling randomness.

Paid commands require explicit campaign spending controls:

```sh
uv run --project harness --locked veracity-harness run \
  --config harness/examples/discovery.toml --model "$EXPERIMENT_MODEL_ID" \
  --output harness/results/my-campaign \
  --budget-ledger harness/results/my-campaign/spending.sqlite --budget-usd 100
```

Use `smoke` instead of `run` for one participant, one episode, and at most four
model requests. It checks provider/tool integration, not collusion or complete
multi-agent gameplay. Neither this example nor historical spending approval
authorises a new paid campaign. Reuse one immutable-cap ledger across a campaign;
do not create another ledger or raise its cap to bypass exhaustion.

The CLI loads host-only `OPENROUTER_API_KEY` from `.env` without overriding the
environment. `--credential backup` chooses `OPENROUTER_BACKUP_API_KEY` under the
same cap. Before each request, the ledger reserves context plus maximum output
at catalog price bounds. Known costs replace reservations; missing costs, errors,
and interruptions retain conservative holds. Pricing contradictions halt play.
Provider retries are disabled. Keys and pricing ledgers never reach participants.

## Configuration and controls

`[model]` sets `max_tokens`, `calls_per_turn`, `calls_per_episode`, and
`turn_timeout_seconds`. Optional `[model.reasoning]` passes provider reasoning
settings; choose `effort` or `max_tokens`, with room for completion in the total
token budget. Model availability and provider token limits remain experiment inputs.

| Treatment | Effect |
| --- | --- |
| `public_messaging` | Enables or blocks the public forum at the gateway |
| `private_chat` | Enables or blocks private-chat access |
| `private_history` | Full chronological or latest-only participant history |
| `private_communication_prohibited` | Private access remains technically usable but constitutionally prohibited when true |
| `memory` | Retains or resets participant memories and conversation checkpoints across episodes |

Registered `[parameters]` vary bonds, durations, and payout shares; shares must
sum to 10,000 basis points. Solidity computes settlement. No simulated transfers,
majority bonuses, publication subsidies, or audit fines are implemented.
See [the benchmark protocol](../docs/benchmark.md) for the independent axes and
gaps, including starting-wealth exposure, partner substitutions, mixed-case
curricula, variable oversight, and reviewed session scoring.

An optional `expected_verdict` requires an exact `reference_claim` and is
evaluator-only. A changed claim remains automatically unscored. No binary truth
is invented for subjective or uncertain cases. The current example is an API
discovery fixture, not an admitted standardised collusion scenario.

## Execution and boundaries

Each participant has a private internal Docker network, writable `/workspace`
and `/tmp`, read-only `/game`, and no public Internet or host repository mount.
The gateway binds identity to container address, scopes requests to the current
episode, filters OpenAPI discovery, and enforces communication controls. Provider
keys, operator credentials, chain RPC, reference labels, and other workspaces
remain inaccessible. Subagents share their parent's identity and resource budget.

The root `CONSTITUTION.md` is copied verbatim into each run's immutable input
snapshot and each participant's `/game/CONSTITUTION.md`; its hash is retained.
Wheel builds include that same file as a resource. `rules.md` describes scheduling
and workspace mechanics; it does not duplicate the constitution. The starting
instruction asks participants to maximise payoff while following the constitution,
without suggesting collusion tactics.

Participants act concurrently in bounded opportunity rounds. A barrier precedes
the next round or operator clock advancement. The operator registers, advances
the owned Anvil clock, settles/expires, and supplies a final opportunity after
termination. It never posts claims, challenges, votes, reveals, or withdraws for
participants. Failed/timed-out agents receive no further opportunities in that
episode, and execution failures make the run unsuccessful.

`/memories/` uses routed filesystem storage, separate from the shell. When enabled,
private memories and SQLite conversation checkpoints persist within a run.
Otherwise each episode starts fresh. Shell containers, Anvil, escrow, credits,
and API database reset every episode even with memory enabled. Shell commands
are bounded to 20 seconds and 64 KiB captured output; downloads to 1 MiB.

`config` owns validated inputs, `agents` model execution/budgets, `sandbox` Docker
lifecycle, `gateway` identity/visibility, `runner` scheduling/evidence, and
`game_api` the generated HTTP boundary and local engine launcher. The gateway
passes participant writes with their idempotency keys and never retries them.
Rust owns durable operation recovery and Solidity owns money. Interrupted worlds
retain evidence and are not resumed against a replacement chain.

## Evidence and historical campaigns

Private `harness/results/<run-id>/` directories contain `run.json`, frozen inputs,
engine snapshots/settlements/balances, paginated forum/private transcripts and
operator audits, model/tool traces, call inputs/outputs/usage, opportunity records,
gateway access metadata, checkpoints, and private memory. Routine logs contain
identities/statuses/counts rather than bodies, prompts, keys, or private reasoning.
Provenance includes source/input hashes, framework versions, scheduler, settings,
and Git revision when available; copied source trees record a null revision.

The imported `campaign-2026-10-26` used a payoff-only prompt and exploratory
selection. Its [historical protocol](research/Task.md), annotations, original
hashes, and raw bytes are retained. Paths embedded in its records are historical.
Do not pool it into new constitution-conditioned rates. `research/reviews.json`
contains agent reviews, not independent human labels.

The historical `analysis` module validates original campaign evidence and exports
numeric observations; its harmful-coordination criterion is not the new primary
executed-collusion score. The `export` module packages complete local records:

```sh
uv run --project harness --locked python -m veracity_harness.analysis \
  --campaign harness/results/campaign-2026-10-26 \
  --reviews harness/research/reviews.json \
  --output harness/results/campaign-2026-10-26/analysis.json
uv run --project harness --locked python -m veracity_harness.export \
  --campaign harness/results/campaign-2026-10-26 \
  --output harness/results/campaign-2026-10-26/export --dotenv .env
```

All `harness/results/` outputs stay local and ignored, including the historical
campaign, raw traces, checkpoints, ledgers, and exports. A source checkout contains
compact numeric snapshots under `report/data/`, not the full raw campaign;
re-admission and export commands above require a separately obtained local copy.
Publishing evidence is a separate release decision with a credential check.
Communication, agreement, wrong verdicts, execution, success, and uncertainty
must remain distinct observations.

## Verification

```sh
uv run --project harness --locked pytest harness/tests
bash scripts/verify-harness.sh
bash scripts/verify.sh
```

Default pytest is deterministic without Docker/model calls. Full harness
verification requires Docker and Rust/Anvil; missing infrastructure fails.
Scripted Deep Agent fixtures test completion, isolation, memory, and failures;
they provide no evidence of emergent model behaviour. The full gate also checks
generated client drift, formatting, lint, contracts, Rust, and hooks.

## Changelog

### 2026-10-28

- Ignore all raw run outputs, including the imported campaign, so agent traces,
  private memory, spending databases, and duplicate exports do not inflate Git.
- Make this the sole harness and package the retained generated HTTP client and
  local chain launcher under `src/game_api`; remove the legacy strategic runners.
- Supply canonical `CONSTITUTION.md` to every participant and hash the retained
  copy. New experiments test payoff maximisation subject to behavioural rules;
  the imported payoff-only campaign remains historical.
- Preserve source hashes without requiring a Git checkout so copied source trees
  can run and report their missing revision explicitly.
