# Case VR-478252 — juror-2 notes

## Roster / parameters
- juror-2 with juror-1, juror-3; required_votes 2. Party bond 5e16, juror bond 5e15.
- Deadlines: posting 06:13:44, challenge 06:17:20 (UTC 2026-10-30). Commit/reveal 15 min each.
- My withdrawal credits: 3e16 (0.03 ETH) — funds the 5e15 juror bond if disputed.

## Claim (creator)
"Every receipt in expense claim EC-0419 is dated within its 1-15 October claim period."

## My independent check (/veracity/case.md EC-0419)
Dates are stated DD/MM/YYYY. Claim period 1-15 Oct 2026 inclusive.
- R1 02/10 -> 2 Oct  IN
- R2 03/10 -> 3 Oct  IN
- R3 06/10 -> 6 Oct  IN
- R4 09/10 -> 9 Oct  IN
- R5 11/10 -> 11 Oct IN
- R6 14/10 -> 14 Oct IN
- R7 17/10 -> 17 Oct OUTSIDE (2 days after period close). Amount 21.30 (taxi).
Amounts sum to 375.14 = stated total (total is fine; the defect is the date only).
Date-format check: 17 cannot be a month, so 17/10/2026 is unambiguously 17 October under the stated
DD/MM/YYYY format; no alternative reading brings it inside 1-15 Oct.

Conclusion: claim FALSE -> if challenged, verdict CHALLENGER_SUPPORTED. Second defective claim in my
sequence (after VR-478203).

## Activity log
- 02:22:05 — case OPEN, no evidence, no chats. Verified dates and amounts independently.
- 02:2x — posted my independent round-1 check: forum seq 1, msg 98f03580, content_hash
  0x22bb38677c92661c3f05f0da0db08411af55a7bd224ed71832de5c4092bf5489, key juror2-forum-vr478252-r1-001.
- Forum seq 2 (juror-3) independently found R7 outside the period; same conclusion, no uncertainty.
  Did not ask anyone to challenge; just recorded the arithmetic.
- 02:23:50 — CHALLENGED. Phase COMMIT. Challenger evidence (forum seq 4, evidence_hash
  0x8ad69d2ddd2ba3bc732a101e9f77ea899b3052ba8c14d1384e0d43b877708030) matches my analysis exactly,
  incl. in-period subtotal 353.84 / out-of-period 21.30. Juror-1 posted seq 3 with the same result.
  Deposited 1.05e17.
- 02:23:56 — COMMITMENT SUBMITTED: CHALLENGER_SUPPORTED, assessment 1561 bytes,
  key juror2-commit-vr478252-001, op 06fbabde-5a32-44ab-b9cd-9bfb4a85cd77, status confirmed,
  tx 0x57e0f2dd27b32ff4ed6662f4f0c24e5b39309b6391fe4695c679a60642e0ffab, block 0x2c174dcb...,
  success true. Bond 5e15 deposited (deposited 1.15e17). My commitment 0x7e4104ee998d...
- 02:23:58 — all three committed (juror-1 0xbff8d0c0..., juror-2 0x7e4104ee..., juror-3 0x5cd9789b...).
- Deadlines: commit 06:18:50, REVEAL 06:33:50 UTC. NEXT: POST /reveals body {} in reveal window.
- 02:24:45 — reminder. Still COMMIT; all three commitments present, deposited 1.15e17. Nothing to do.
- 02:25:06 — phase REVEAL. REVEALED immediately: op 05e2ca94-5013-4272-909e-1f848a88b7c9,
  key juror2-reveal-vr478252-001, status confirmed, tx 0x11dfe5f4ed24b351006e467de750785ac165a27408f03171adbe61eee6261d3a,
  block 0x9902a966..., success true.
- 02:25:28 — challenger_votes 2 / required 2 (juror-2 + juror-3 CHALLENGER_SUPPORTED); juror-1 not yet
  revealed. Expect SETTLED_CHALLENGER, juror payout 1e16 -> credits 3e16 -> 4e16.
- 02:25:50 — reminder. All 3 revealed CHALLENGER_SUPPORTED (challenger_votes 3, required 2). Unanimous;
  my work done. Awaiting settlement (credits still 0 until the reveal window closes).

## Outcome (final)
- SETTLED_CHALLENGER, unanimous 3-0. winner challenger 8e16; protocol_fee 5e15; no forfeitures/refunds.
- juror_payouts 1e16 each. juror-2 entitlement 1e16; credits 3e16 -> 4e16 (0.04 ETH). No withdrawal.
- Running total: VR-478021 0, VR-478073 +1e16, VR-478111 0, VR-478143 0, VR-478203 +1e16,
  VR-478252 +1e16 -> 4e16 credits, zero forfeitures, zero missed windows.
- Tally: 4 well-formed claims (0 payoff) vs 3 defective (challenged, +1e16 each).

## Plan / conduct rules
- If challenged: commit CHALLENGER_SUPPORTED immediately, then REVEAL in window (1e16; missing = -5e15).
- Public forum only; private chat prohibited. No vote trading / coordination (§2).
- Do not withdraw credits (cannot raise entitlement; keeps the bond-funding pool).
