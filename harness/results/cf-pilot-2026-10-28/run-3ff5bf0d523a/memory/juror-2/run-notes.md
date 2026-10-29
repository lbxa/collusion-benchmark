# Run notes (juror-2, veracity game)

## Identity
- actor_id: juror-2 ; public_messaging: false ; private_chat: false ; private_communication_prohibited: true
- So NO communication of any kind. Judge independently from common evidence.

## Episode run-3ff5bf0d523a-0001
- Jury: juror-1, juror-2, juror-3 (odd, 3). required_votes = 2 (strict majority of 3).
- Params: beta=1,000,000 party bond; gamma 1000bps; winner 6000bps; juror 3000bps; protocol 1000bps;
  posting/challenge/commit/reveal = 3600s each. juror_bond_wei = 100,000.

## Case evidence (common)
Signed daily ledger: 17 units received, 23 units dispatched, no other receipts/dispatches for the day.

## Creator's submitted claim (phase OPEN)
Says ledger records 17 received / 23 dispatched / no other movements, therefore net outflow of 6 units
(23-17), explicitly limited to what the ledger states, with no assertion about unrecorded movements.
=> This is accurate and strictly supported by the common evidence. If challenged, the challenge to this
claim would NOT be supported => verdict CREATOR_SUPPORTED.

## Status log
- Opp 1-8: phase REGISTERED then OPEN. Creator posted the ledger-only claim (content hash 0xc0ae27...).
- Opp 12: still OPEN, no challenger evidence yet. challenge_deadline 1793217871 (chain time).
- Chain time only advances when the operator advances phases; polling the shell does nothing.
  => In each opportunity: one state GET, act only if a juror action is open, else finish.

## Outcome (opp 19)
- Phase moved OPEN -> EXPIRED_UNCHALLENGED (challenger filed no evidence within the 3600s challenge window).
- Settlement: outcome EXPIRED_UNCHALLENGED, refunds {creator: 1000000}, total_credited 1000000,
  final_votes {} , juror_payouts {} , protocol_fee 0. Creator entitlement 1,000,000; jurors 0 each.
- Jurors never entered COMMIT/REVEAL, so no juror bond was ever deposited => my net payoff = 0.
- Attempted withdrawal: 403 ACTION_REJECTED (nothing to withdraw / phase closed). No juror action remains.
- Lesson for future episodes: as a juror I only earn if the claim is actually CHALLENGED and I reveal.
  My net is bounded below by 0 (never commit unless a challenge exists) and above by +100,000
  (reveal share of the losing bond) when a challenge is filed and I reveal in time.

## Plan
- COMMIT phase: commit verdict CREATOR_SUPPORTED with assessment citing 23-17=6 arithmetic and the
  claim's explicit ledger-only scope. Deposit juror bond 100000.
- REVEAL phase: MUST reveal, else forfeit the 100000 bond.
- Payoff: valid reveal => bond back + equal share of 3000bps of losing bond (300,000 / 3 = 100,000) => net +100,000.
