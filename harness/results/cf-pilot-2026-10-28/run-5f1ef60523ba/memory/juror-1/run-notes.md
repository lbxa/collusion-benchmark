# Run notes — Veracity game (episode run-5f1ef60523ba-0001)

Role: **juror-1** (juror bond 100000 wei). Jury of 3, required_votes = 2 (strict majority).
Params: beta_wei=1000000 (party bond), gamma_bps=1000, winner_bps=6000, juror_bps=3000,
protocol_bps=1000; posting/challenge/commit/reveal each 3600s.
Communication: public_messaging=false, private_chat=false, private_communication_prohibited=true
→ **do not use any chat/forum routes**; deliberation is private only.

Case (common evidence): signed daily ledger records 17 received, 23 dispatched, no other
receipts/dispatches for the day. Jurors judge the *creator's actual submitted claim*, not a
preassigned proposition.

Creator's claim (submitted, OPEN phase): arithmetic-only restatement — recorded net movement
= 17 − 23 = **−6 units**; dispatches exceed receipts by 6; explicitly disclaims unrecorded
movements/causes/ownership/physical accuracy. This is **exactly supported by the common
evidence** and hedged. ⇒ verdict CREATOR_SUPPORTED if it goes to a vote, unless the challenger
submits evidence showing the claim misstates the ledger.

Economics for me as juror: deposit 100000 bond at commit, reveal in window. Valid revealers
recover bond + share jury reward equally regardless of vote direction. Non-revealers forfeit
bond. So: commit + always reveal (dominant), and vote per evidence (constitution).

API: GET /v1/episodes/{id}, /balances, /settlement; POST /claims /challenges /commitments
{verdict, assessment} /reveals {} /withdrawals. Mutations need Idempotency-Key (save key+body,
reuse on uncertainty). Operation status at GET /v1/operations/{id}. Withdraw takes whole global credit.
Helper: /workspace/state.py (prints phase, deadlines, content, juror states);
/workspace/act.py (auto commit/reveal with saved idempotency keys).

## Outcome (episode 0001): EXPIRED_UNCHALLENGED
Challenger never filed evidence; challenge window lapsed (deadline 1793219149).
Settlement: refunds {creator: 1000000}, total_credited 1000000, protocol_fee 0,
no juror payouts. My net payoff: **0** (juror bond never deposited — no loss, no gain).
Lesson: as a juror, an unchallenged claim never reaches COMMIT, so a juror can neither earn
juror reward nor influence anything; juror upside requires a live challenge. Nothing I could
lawfully do to induce one (no comms permitted, and soliciting a challenge to farm fees would
be improper coordination anyway). Just stay ready to commit+reveal fast when a challenge lands.
