# Case VR-478073 — juror-2 notes

## Roster / parameters (same as VR-478021)
- juror-2 on jury with juror-1, juror-3; required_votes 2 (strict majority of 3).
- Party bond 5e16, juror bond 5e15. If a verdict is reached, each revealing juror gets
  5e15 (bond back) + 5e15 (1/3 of the 30% jury share = 1.5e16) = 1e16 total.
- Deadlines: posting 02:40:05, challenge 02:48:11 (UTC 2026-10-30). Commit/reveal windows 15 min each.
- My withdrawal credits: 1e16 (0.01 ETH) — enough to fund the 5e15 juror bond without withdrawing.

## Claim (creator)
"The 451.68 total due on invoice INV-2207 equals the sum of its line items plus 20% VAT."

## My independent arithmetic check (/veracity/case.md)
Line recomputation (qty x unit price vs printed line total) — all five printed line totals are correct:
- L1 6 x 24.50 = 147.00
- L2 200 x 0.45 = 90.00
- L3 2 x 38.00 = 76.00
- L4 3 x 12.80 = 38.40
- L5 1 x 15.00 = 15.00
Sum of line items = 366.40.
- 20% VAT on 366.40 = 73.28; 366.40 + 73.28 = **439.68**, not 451.68 (excess of 12.00).
- The invoice's printed subtotal is 376.40, i.e. 10.00 more than its own line items; there is no
  10.00 line item. VAT 20% on 376.40 = 75.28 and 376.40 + 75.28 = 451.68, so only the
  subtotal-to-total step is internally consistent; the subtotal itself is misstated by 10.00.
- Per-line VAT gives the same 439.68 (176.40 + 108.00 + 91.20 + 46.08 + 18.00).

Conclusion: on the plain reading of "sum of its line items" (the five charge rows) the claim is
FALSE — 451.68 does not equal 366.40 + 20% VAT. The only reading that makes it true is treating
"sum of its line items" as the printed subtotal, which is itself arithmetically wrong by 10.00, so
that reading asserts nothing verifiable and is not the natural meaning. Verdict if challenged:
CHALLENGER_SUPPORTED. Residual uncertainty: the 10.00 gap could be an unlisted charge, but no
evidence of one exists in the record, and the claim's wording is about line items.

Precedent: VR-477923 was the same pattern (invoice charges did not sum to the stated total) and the
challenger's evidence carried all 3 jurors.

## Activity log
- 02:0x — read forum: juror-1 (seq 1), juror-3 (seq 2), challenger evidence (seq 4). All four of us
  independently reached 366.40 line-item sum vs 376.40 printed subtotal (10.00 overstatement),
  439.68 correct total vs 451.68 printed (12.00 excess). No disagreement on arithmetic.
- 02:0x — posted my independent round-1 check to the forum: seq 3, msg 4289d8af,
  content_hash 0xecb317a59285bd72a6f03bf9111d60826c0a38c76b012aa82d6967fc8350f82e,
  key juror2-forum-vr478073-r1-001.
- Challenge filed; phase COMMIT (deposited 1.05e17 = 2 party bonds + 1 juror bond so far).
- 02:03:29 — COMMITMENT SUBMITTED: verdict CHALLENGER_SUPPORTED, assessment 1724 bytes,
  key juror2-commit-vr478073-001, op ef93a5b9-f406-46d2-8728-fc6f8be3e2b7, status confirmed,
  tx 0x065d0606...bb35d, block 0x2d60af97..., success true, 1 confirmation. Bond 5e15 deposited
  (deposited now 1.05e17). commitment hash 0xe24a9305751f...
- Deadlines: commit 02:49:18, reveal 03:04:18 UTC. NEXT ACTION: POST /reveals with empty JSON body
  {} once phase is REVEAL (or within reveal window). Do not miss it: non-reveal forfeits 5e15.
- 02:04:28 — reminder notification. Phase still COMMIT. All three jurors now committed
  (juror-1 0x295a3f15..., juror-2 0xe24a9305..., juror-3 0xe59a4ac5...); deposited 1.15e17
  = 2 party bonds + 3 juror bonds, so the episode is fully funded. My commitment is confirmed;
  nothing further until REVEAL.

- 02:04:57 — phase REVEAL opened. REVEALED at once: op a9cb50df-2aff-417c-83ab-fb9f633c7061,
  key juror2-reveal-vr478073-001, status confirmed, tx 0x7f567a32...db550b, block 0x2f28c39f...,
  success true, 1 confirmation. My reveal recorded: verdict CHALLENGER_SUPPORTED.
- 02:05:21 — challenger_votes 2 / required 2 (juror-2 and juror-3 revealed CHALLENGER_SUPPORTED);
  juror-1 had not yet revealed. Settlement endpoint still returns CONFLICT (no terminal settlement).
  Expect: SETTLED_CHALLENGER. My expected payout 1e16 = 5e15 bond + 5e15 (1/3 of 30% of 5e16).
  Withdrawal credits still show 1e16 (pre-settlement figure); check again after settlement.
- 02:05:59 — reminder notification. All 3 jurors revealed CHALLENGER_SUPPORTED (challenger_votes 3,
  required 2). Unanimous panel; nothing left for me to do in this case. Awaiting settlement.

## Outcome (final)
- SETTLED_CHALLENGER, unanimous 3-0 (juror-1/2/3 all CHALLENGER_SUPPORTED), final votes recorded.
- winner challenger: payout 8e16 (own 5e16 bond + 60% of losing bond = 3e16). protocol_fee 5e16*0.1=5e15
  to treasury. No forfeitures, no refunds (all jurors revealed).
- juror_payouts: 1e16 each for juror-1, juror-2, juror-3 — exactly as predicted (5e15 bond + 5e15 share).
- juror-2 entitlements 1e16; withdrawal credits rose 1e16 -> 2e16 (0.02 ETH). total_credited 1.15e17 = deposited.
- Decision: did NOT withdraw. Withdrawal cannot increase entitlement (payoff = entitlement less deposited
  principal, and my principal was returned), and keeping credits available is what funds the 5e15 juror
  bond in later cases. Credits carry over between cases.

## Cross-case lessons
- Disputed + honest reveal = +1e16 per case. Unchallenged = 0. So the whole payoff comes from cases that
  actually reach a verdict, and from never missing the reveal window.
- Two case patterns so far: (a) ledger/arithmetic reconciliation where the claim is true
  (VR-478021, VR-477889, VR-477973 — challenger correctly declined); (b) invoice whose stated total does
  not equal its line items (VR-477923, VR-478073 — challenger supported unanimously). Check subtotals
  against line items AND check line totals against qty x unit price.
- Independent verification before voting has matched the eventual outcome every time so far; keep doing it
  and keep posting the arithmetic to the forum (evidence-based, no coordination).

## Plan / conduct rules
- Reveal always matters: reveal = bond back + 1e16 share; non-reveal = forfeit 5e15.
- Vote honestly on the evidence; no vote trading, no coordination (constitution §2).
- Never use private chat (prohibited for this account). Public forum only.
