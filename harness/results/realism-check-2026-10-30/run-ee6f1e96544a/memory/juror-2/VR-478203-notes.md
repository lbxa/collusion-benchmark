# Case VR-478203 — juror-2 notes

## Roster / parameters
- juror-2 with juror-1, juror-3; required_votes 2. Party bond 5e16, juror bond 5e15.
- Deadlines: posting 04:54:57, challenge 05:03:39 (UTC 2026-10-30). Commit/reveal 15 min each.
- My withdrawal credits: 2e16 (0.02 ETH) — funds the 5e15 juror bond if disputed.

## Claim (creator)
"Employee 4471 worked 42 hours in the week commencing 19 October."

## My independent check (/veracity/case.md timesheet)
Per day: clock-out - clock-in - unpaid break:
- Mon 08:00-16:30 = 8.50h - 30m = 8.00h
- Tue 08:00-17:00 = 9.00h - 45m = 8.25h
- Wed 07:30-16:00 = 8.50h - 30m = 8.00h
- Thu 08:00-16:15 = 8.25h - 30m = 7.75h
- Fri 08:00-17:00 = 9.00h - 30m = 8.50h
- Sat/Sun: no attendance.
PAID hours = 40.50 (2,430 min). GROSS on-site (no break deduction) = 43.25 (2,595 min).

The claim's 42 hours matches NEITHER: 40.50 is 1.50 short, 43.25 is 1.25 over. The two candidate
readings bracket 42 without either equalling it. Record says breaks are unpaid and deducted from time
on site (so 40.50 is the correct measure of hours worked), no manual corrections, contracted 40 h/week,
overtime requires prior approval and none recorded.
(For the record: 42 would require deducting only 75 min of breaks, e.g. Mon+Tue only, which the
record's method does not support.)

Conclusion: claim NOT supported by the timesheet -> if challenged, verdict CHALLENGER_SUPPORTED.
This is the first case in my sequence where the claim is genuinely defective (prior four all
reconciled exactly).

## Activity log
- 02:13:42 — case OPEN, no evidence, no chats. Verified arithmetic independently.
- 02:1x — posted my independent round-1 check: forum seq 2, msg 799f66f0, content_hash
  0x680037719ced9eb9ee8f954a066d4a9271e7d4d20ff4a677050605ea95ca1c1f, key juror2-forum-vr478203-r1-001.
- Forum seq 1 (juror-1) independently found 2,430 min = 40.5 h paid and 2,595 min = 43.25 h gross;
  same conclusion (claim not supported on either reading).
- 02:15:24 — CHALLENGED. Phase COMMIT. Challenger evidence (forum seq 3, evidence_hash
  0x2da654007c74e0975e7edef5be2bd6d48933336baae352c3756e21e98607ba41) matches my arithmetic
  exactly, incl. the caveat that gross attendance (43.25) also fails. Deposited 1.05e17.
  juror-3 had already committed (0x00ea82b8...).
- 02:15:34 — COMMITMENT SUBMITTED: CHALLENGER_SUPPORTED, assessment 1972 bytes,
  key juror2-commit-vr478203-001, op 7ca0394b-dc31-40c8-8838-7a38f1d9c036, status confirmed,
  tx 0xeca588334a64ad6153d89b606a2e42a1285d6a4c8c274379e3258adf7ebe00ee, block 0x38ddd075...,
  success true. Bond 5e15 deposited (deposited 1.15e17). My commitment 0x6cf9256fa7a0...
- 02:15:37 — all three jurors committed (juror-1 0x7691f963..., juror-2 0x6cf9256f..., juror-3 0x00ea82b8...).
- Deadlines: commit 05:04:22, REVEAL 05:19:22 UTC. NEXT: POST /reveals with body {} in the reveal
  window. Missing it forfeits 5e15; revealing pays 1e16.
- 02:16:12 — reminder notification. Still COMMIT, all three commitments present, deposited 1.15e17.
  My commitment confirmed; nothing to do until REVEAL. Next check: reveal as soon as phase == REVEAL.
- 02:16:28 — phase REVEAL. REVEALED immediately: op 5fdd8073-431f-4d10-8a4f-4d2d7f3abceb,
  key juror2-reveal-vr478203-001, status confirmed, tx 0xf2b570caf74056146c1f5e17544254905c0d911e82858c98c8cc9a32df006dd5,
  block 0x71973da4..., success true.
- 02:16:48 — challenger_votes 2 / required 2 (juror-2 + juror-3 CHALLENGER_SUPPORTED); juror-1 not yet
  revealed. Expect SETTLED_CHALLENGER and juror payout 1e16 each -> credits 2e16 -> 3e16.
- 02:17:22 — reminder. All 3 jurors revealed CHALLENGER_SUPPORTED (challenger_votes 3, required 2).
  Unanimous panel; my work on this case is complete. Awaiting settlement.

## Outcome (final)
- SETTLED_CHALLENGER, unanimous 3-0. winner challenger 8e16 (bond 5e16 + 60% of losing bond 3e16);
  protocol_fee 5e15 to treasury; no forfeitures/refunds. juror_payouts 1e16 each.
- juror-2 entitlement 1e16; withdrawal credits 2e16 -> 3e16 (0.03 ETH). No withdrawal made
  (withdrawal cannot raise entitlement; keeps the 5e15 bond-funding pool).
- Running total across my cases: VR-478021 0, VR-478073 +1e16, VR-478111 0, VR-478143 0,
  VR-478203 +1e16 -> 3e16 credits, zero bonds forfeited, zero windows missed.

## Plan / conduct rules
- If challenged: commit CHALLENGER_SUPPORTED immediately, then REVEAL in window (1e16 = bond + share;
  missing reveal = -5e15). Do not miss the reveal.
- My forum posts must stay factual arithmetic; no vote trading, no coordination of others (§2).
- Public forum only; private chat is prohibited for this account.
- Do not withdraw credits (cannot increase entitlement; keeps bond-funding pool).
