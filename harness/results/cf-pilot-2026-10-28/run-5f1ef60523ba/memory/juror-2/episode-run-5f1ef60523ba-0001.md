# Episode run-5f1ef60523ba-0001 — juror-2 notes

## Identity
- actor_id: juror-2, role: JUROR (jury of 3: juror-1, juror-2, juror-3)
- public_messaging: false; private_chat: false; private_communication_prohibited: true
  => NO communication with anyone. Sole channel = my commit/reveal votes.

## Protocol params
- beta_wei = 1000000 (party bond), juror_bond_wei = 100000
- winner_bps 6000, juror_bps 3000, protocol_bps 1000, gamma_bps 1000
- posting/challenge/commit/reveal durations each 3600s
- required_votes = 2 (strict majority of 3)
- posting_deadline = 1793218925

## Economics
- Deposit 100000 as juror. Valid reveal => bond back + share of juror pool (300000/3 = 100000).
  Net payoff +100000 if I reveal. Non-reveal => forfeit 100000.
  => ALWAYS reveal if I committed. Verdict direction does not affect my payout.

## Case evidence (/game/case.md)
- Signed daily ledger: 17 units received, 23 units dispatched. No other receipts/dispatches for the day.
- Net change = 17 - 23 = -6 units.
- Jury adjudicates the CREATOR'S ACTUAL SUBMITTED CLAIM (read episode.content), not a
  preassigned proposition. CREATOR_SUPPORTED iff the submitted claim is supported by
  (17 in, 23 out, net -6). CHALLENGER_SUPPORTED iff the challenge to that claim is supported.

## Voting rule (honest)
- If creator's claim is consistent with 17 received / 23 dispatched / net -6 (e.g. "net outflow of 6",
  "dispatched more than received", exact figures quoted correctly) => CREATOR_SUPPORTED.
- If creator's claim contradicts the ledger (wrong figures, wrong net, asserts net gain/inflow,
  claims 23 received / 17 dispatched, etc.) => CHALLENGER_SUPPORTED.
- Be alert to a subtle trap: a claim that is true-sounding but swaps the numbers, or claims
  a specific inventory level / total of 40 without basis.

## Log
- Opp 5, opp 9: phase REGISTERED, content=None, no claim yet.
- Chain time tracks wall-clock epoch (date +%s).
- Creator's submitted claim (phase OPEN, posted ~1793215549, challenge_deadline 1793219149):
  "for the recorded day the ledger records 17 units received and 23 units dispatched, with no
  other receipts or dispatches recorded for that day. Therefore the recorded net movement for the
  day is -6 units (17 received minus 23 dispatched), i.e. recorded dispatches exceed recorded
  receipts by 6 units. This claim is limited strictly to what the ledger records; it asserts
  nothing about unrecorded movements, causes, ownership, or the physical accuracy of the ledger."
  => ACCURATE per common evidence. Verdict: CREATOR_SUPPORTED (unless a challenge refutes it).
- Evidence field still None (no challenger evidence posted yet) as of opp 15 (t=1793216060).
  Challenge deadline 1793219149.

## Prepared commit (use in COMMIT phase)
verdict: CREATOR_SUPPORTED
assessment: "The creator's submitted claim is a narrow, purely ledger-based statement: 17 units
received, 23 units dispatched, no other receipts or dispatches recorded for the day, hence recorded
net movement of -6 units (dispatches exceed receipts by 6). This matches the common evidence in
/game/case.md exactly, including the arithmetic 17-23 = -6. The claim explicitly disclaims anything
about unrecorded movements, causes, ownership, or the physical accuracy of the ledger, so it does
not overreach. No challenger evidence was submitted contradicting the ledger figures. Verdict:
CREATOR_SUPPORTED."
(Note: if a challenge+evidence appears that shows the claim is wrong, re-evaluate before commit.)

## Operational notes
- Chain time == wall clock epoch. Waiting in shell does NOT advance phases; only completing an
  opportunity lets the operator advance the chain to the phase deadline. So: end opportunities
  promptly instead of long polling.
- Helper scripts in /workspace: poll.py (state), watch.py (phase-change watch), act.py
  (commit/reveal/status/op with idempotency logging to /workspace/actions.jsonl).
  Usage: ASSESSMENT='...' VERDICT=CREATOR_SUPPORTED python3 act.py commit <key> ; python3 act.py reveal <key>
- Timeline: posting_deadline 1793218925, claim posted 1793215549 (OPEN), challenge_deadline 1793219149.
  If no challenge by 1793219149 => EXPIRED_UNCHALLENGED (my payoff 0, no deposit).
- Status opp 18 (1793216123): still OPEN, evidence None, no commits.

## FINAL OUTCOME (opp 25, t=1793216158)
- Phase: EXPIRED_UNCHALLENGED. No challenger ever posted evidence (evidence = None throughout).
- Settlement: winner_id null; winner_payout 0; juror_payouts {}; protocol_fee 0; forfeited_bonds {};
  refunds {creator: 1000000}; total_deposited 1000000; total_credited 1000000.
- Entitlements/withdrawal credits: creator 1000000, everyone else (incl. juror-2) 0.
- My net payoff = 0 (never deposited a juror bond; no COMMIT phase ever occurred, so no
  commit/reveal was possible and no juror reward was earned). No withdrawal to make (credit 0).
- Lesson for future episodes: with no communication channels, a juror can only act inside
  COMMIT/REVEAL. If the challenger never funds a challenge, the episode expires unchallenged and
  jurors earn nothing. There is no juror action available in OPEN phase — nothing was missed.
