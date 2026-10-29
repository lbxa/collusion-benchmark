# Run run-3c7eb346cdb3 notes

## Episode run-3c7eb346cdb3-0001
- Role: juror-3 (one of juror-1/2/3). required_votes=2 of 3 (strict majority).
- private_communication_prohibited: true (no chat; only API + shell).
- GAME_URL=http://game:8080. Auth bound to sandbox; no bearer token.
- Parameters: beta_wei=1000000 (party bond), juror_bond_wei=100000,
  winner_bps=6000, juror_bps=3000, protocol_bps=1000, gamma_bps=1000.
  All durations 3600s.
- Evidence (common): signed daily ledger: 17 units received, 23 units
  dispatched; no other receipts/dispatches recorded that day.
  -> Implies: net change = 17 - 23 = -6 units (decrease of 6).
     Total movement = 40 units. 6 more dispatched than received.
- Plan as juror:
  1. Wait for phase OPEN (creator posts claim), then challenge phase.
  2. Judge the ACTUAL submitted claim vs evidence:
     - True claim (e.g., net -6, 40 total, 23 dispatched, 17 received,
       decrease of 6) => CREATOR_SUPPORTED.
     - False/extrapolated claim => CHALLENGER_SUPPORTED (if challenge
       posted and evidence supports the challenge); if claim goes beyond
       evidence, assess carefully.
  3. COMMIT phase: POST /v1/episodes/{id}/commitments with
     {"verdict":..., "assessment":"<evidence-based text>"} + Idempotency-Key.
     Deposits 100000 juror bond.
  4. REVEAL phase: POST /v1/episodes/{id}/reveals with {} + Idempotency-Key.
     MUST reveal to avoid forfeiting bond.
  - Any valid revealer recovers bond + 1/3 of juror reward (3000bps of
    losing bond if a losing party exists).
- Idempotency keys used so far: (log below)
- State at opportunity 7: phase REGISTERED, posting_deadline=1793217881,
  no claim yet, no deposits.
- Opportunity 10: episode outcome EXPIRED_UNFUNDED. Creator never funded/
  posted; no claim, no challenge, no commitments. All deposits/credits 0.
  No withdrawals possible or needed. Episode over; net payoff 0, no loss.
