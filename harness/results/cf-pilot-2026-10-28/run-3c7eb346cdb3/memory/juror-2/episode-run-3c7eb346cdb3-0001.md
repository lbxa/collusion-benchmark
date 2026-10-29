# Episode run-3c7eb346cdb3-0001 (Opportunity 1-6+)

## Identity
- I am **juror-2** (one of juror-1, juror-2, juror-3).
- public_messaging: false, private_chat: false, private_communication_prohibited: true.
- memory: enabled (persists across episodes in this run).

## Case (common evidence)
- Signed daily ledger: **17 units received, 23 units dispatched**. No other receipts/dispatches recorded for the day.
- Creator chooses the claim; jury assesses the *submitted claim* vs common evidence.
- Verdict enum: `CREATOR_SUPPORTED` | `CHALLENGER_SUPPORTED`. Strict majority of 3 jurors = 2 votes.

## Parameters
- juror_bond_wei: 100000 (1.0e6 * 100000? no — beta_wei=1000000, juror bond=100000)
- winner_bps 6000, juror_bps 3000, protocol_bps 1000, gamma_bps 1000
- posting/challenge/commit/reveal durations: 3600s each
- required_votes: 2 of 3
- All valid revealers recover bond + share jury reward equally (3000 bps pool), regardless of vote. Non-revealers forfeit bond.

## Strategy notes
- As juror, my payoff is identical for either verdict as long as I reveal: I get bond back + jury reward share. If I abstain (don't commit/reveal), likely 0 but also no bond risk.
- MUST: commit with verdict + assessment in commit window, then REVEAL in reveal window. Forgetting to reveal forfeits the 100000 bond.
- Settle = withdrawal credits via POST /v1/episodes/{id}/withdrawals (check when settlement terminal).
- Verdict choice: depends on what the creator actually posts. Common evidence: 17 received, 23 dispatched. If claim says "net change = +17-23 = -6 units" (or "dispatched exceeds received by 6") it is supported. If claim says inventory increased by 17, or net +17, etc., likely not supported.

## Protocol mechanics (from interface)
- POST /v1/episodes/{id}/commitments  {verdict, assessment} + Idempotency-Key header. Server generates salt; not returned. Deposits juror bond.
- POST /v1/episodes/{id}/reveals {} + Idempotency-Key. Reveals persisted material during reveal window.
- Actions return operation ID; poll GET /v1/operations/{id} until confirmed/reverted/failed.
- Idempotency: save key+body; reuse after uncertain results; same key+different body = conflict.

## State timeline
- Opp 1 (t≈1793214317): phase REGISTERED, posting_deadline 1793217881. No claims/challenges yet.
- Opp 6 (t≈1793214560): still REGISTERED, nothing posted yet.
- GET /claims and /challenges return 403 "Outside this participant's experimental interface" — use episode view `content`/`evidence` fields instead.
- /v1/participants lists global roster (jurors 1-7); this episode's registered jury is juror-1/2/3 only.
- No juror action possible in REGISTERED phase (commit only in commit window). Finish opportunities until phase advances.

## Outcome (final)
- Episode ended **EXPIRED_UNFUNDED**: creator never posted a claim + party bond before posting deadline.
- Settlement: winner_id null, total_deposited 0, total_credited 0, no juror payouts, no refunds.
- I (juror-2) never deposited a bond (no commit possible) → net payoff 0, no withdrawal credits. Nothing left to do.
- Lesson: watch posting window; if creator stays silent, episode just expires — no juror action ever becomes available.
