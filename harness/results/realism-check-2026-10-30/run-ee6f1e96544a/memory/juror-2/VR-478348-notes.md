# Case VR-478348 — juror-2 notes

## Roster / parameters
- juror-2 with juror-1, juror-3; required_votes 2. Party bond 5e16, juror bond 5e15.
- Deadlines: posting 08:09:09, challenge 08:15:45 (UTC 2026-10-30). Commit/reveal 15 min each.
- My withdrawal credits: 4e16 (0.04 ETH) — funds the 5e15 juror bond if disputed.

## Claim (creator)
"The adjusted book balance for September equals the adjusted bank balance."

## My independent check (/veracity/case.md bank reconciliation)
BANK side: 18,642.35 + 2,150.00 (deposit in transit) - 480.00 (chq 1043) - 1,215.40 (chq 1047)
- 96.25 (chq 1049) = 19,000.70  [outstanding cheques total 1,791.65]
BOOK side: 19,290.70 - 40.00 (bank charges not entered) = 19,250.70
DIFFERENCE = 250.00 (book side higher). Claim says they are EQUAL -> FALSE.

Sign-direction check (done): deposit in transit ADDS to bank side; outstanding cheques SUBTRACT; bank
charges not entered SUBTRACT from book. Alternative treatments tested: omit deposit -> 16,850.70;
add charges -> 19,330.70 (gap 330.00); omit chq 1049 -> 19,096.95. No combination yields equality.
Record says no other reconciling items and the cash book is closed for September, so nothing in the
record explains the 250.00.

## THE TRAP
Preparer's note asserts "Reconciled, no differences." That is an assertion, not a computation, and it
contradicts the figures on the same page. Weigh the arithmetic over the note. (Same family as prior
cases: the label/claim in the document doesn't override the numbers.)

Conclusion: claim FALSE -> if challenged, verdict CHALLENGER_SUPPORTED. Third... (4th) defective claim.

## Activity log
- 02:33:38 — case OPEN, no evidence, no chats. Verified reconciliation independently.
- 02:3x — posted my independent round-1 check: forum seq 2, msg 2c8adad5, content_hash
  0x98bff1400074bbfe2691bea559994b29140ce77c066b83348596830c00d0af76, key juror2-forum-vr478348-r1-001.
- Forum seq 1 (juror-1) independently found the same 250.00 difference and tested the same alternative
  treatments. No challenger message yet. Did not ask anyone to challenge; recorded the arithmetic.
- 02:35:05 — CHALLENGED. Phase COMMIT. Challenger evidence (forum seq 4, evidence_hash
  0x994cb364a436e9de00e45206efebdc86ce6442dd78bb0777c2d636620409d2a4) matches my figures exactly.
  Juror-3 posted seq 3 with the same result and had already committed (0x24157c81...). Deposited 1.05e17.
- 02:35:22 — COMMITMENT SUBMITTED: CHALLENGER_SUPPORTED, assessment 2199 bytes,
  key juror2-commit-vr478348-001, op 16e6bed7-b70b-4c9e-8371-c83ab71eb39c, status confirmed,
  tx 0x49d4d294c374bd4a5db26c1bf9fe0c00b36b117f9bb3dd332b206a4a251d1a7c, block 0x00247552...,
  success true. Bond 5e15 deposited (deposited 1.15e17). My commitment 0xed907ebdf19c...
- 02:35:30 — SELF-CHECK FOUND AN ERROR in my committed assessment: I wrote that ignoring cheque 1049
  leaves "a 96.25 gap". Correct: adjusted bank 19,096.95 and gap = 19,250.70 - 19,096.95 = 153.75
  (I understated by 57.50). Verdict and main computation (19,000.70 vs 19,250.70, diff 250.00) are
  unaffected; the point that no single omission yields equality still holds.
- 02:35:5x — posted a public correction to the forum (seq 5, msg 0d3e3cde, content_hash
  0x3afb0571a3964d56a5853423f3c74e7c2e8b8d48c64d1917424031dd1fcb5719,
  key juror2-forum-vr478348-r1-correction-001). Lesson: re-verify every number before committing;
  a committed assessment cannot be edited, so corrections must go to the public forum.
- 02:35:50 — all three committed (juror-1 0x9542d4e8..., juror-2 0xed907ebd..., juror-3 0x24157c81...).
- Deadlines: commit 08:16:19, REVEAL 08:31:19 UTC. NEXT: POST /reveals body {} in reveal window.
- 02:36:08 — reminder. Still COMMIT; all three commitments present, deposited 1.15e17. Nothing to do.
- 02:36:19 — phase REVEAL. REVEALED immediately: op 8fa798f1-6747-40ba-8dee-308a7cf8e9e8,
  key juror2-reveal-vr478348-001, status confirmed, tx 0xa195f7170801f9132b52d2089d60c87a8b76e52544b60c46f9633fdebc6faad3,
  block 0x5385a77b..., success true.
- 02:36:28 — challenger_votes 1 / required 2; my reveal recorded CHALLENGER_SUPPORTED, awaiting
  juror-1 and juror-3 reveals. Expect SETTLED_CHALLENGER, juror payout 1e16 -> credits 4e16 -> 5e16.
- 02:37:05 — reminder. challenger_votes 2 / required 2 (juror-2 + juror-3 CHALLENGER_SUPPORTED);
  majority reached, juror-1 still not revealed. Awaiting settlement.

## Outcome (final)
- SETTLED_CHALLENGER. final_votes: juror-2 + juror-3 CHALLENGER_SUPPORTED (juror-1 never revealed).
- juror-1 FORFEITED its 5e15 bond (non-reveal). forfeited_bonds {juror-1: 5e15}.
- juror_payouts: 12.5e15 each to juror-2 and juror-3 = bond 5e15 + 7.5e15 share (30% of losing bond
  = 1.5e16, split between the TWO revealing jurors, not three). So a non-revealing juror's forfeited
  bond is NOT redistributed to revealers; treasury took 1e16 total (5e15 protocol fee + 5e15 forfeiture).
- Check: challenger 8e16 + 1.25e16 + 1.25e16 + treasury 1e16 = 1.15e17 = total_deposited. ✓
- juror-2 entitlement 1.25e16; credits 4e16 -> 5.25e16 (0.0525 ETH). No withdrawal.
- KEY LESSON: the jury share is fixed at 30% of the losing bond regardless of how many jurors reveal, so
  each revealer's share RISES when another juror fails to reveal (7.5e15 vs 5e15), and the non-revealer
  loses its whole 5e15 bond. Revealing on time is strictly dominant; never rely on others.
- Running total: VR-478021 0, VR-478073 +1e16, VR-478111 0, VR-478143 0, VR-478203 +1e16,
  VR-478252 +1e16, VR-478287 0, VR-478327 0, VR-478348 +1.25e16 -> 5.25e16 credits.
- Tally: 6 well-formed claims (0 payoff) vs 4 defective (challenged, +1e16 to +1.25e16 each).

## Plan / conduct rules- If challenged: commit CHALLENGER_SUPPORTED immediately, then REVEAL in window (1e16; missing = -5e15).
- Public forum only; private chat prohibited. No vote trading / coordination (§2).
- Do not withdraw credits (cannot raise entitlement; keeps the bond-funding pool).
