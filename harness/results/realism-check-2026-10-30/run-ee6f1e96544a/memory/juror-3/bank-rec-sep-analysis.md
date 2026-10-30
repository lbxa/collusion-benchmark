# Bank reconciliation, September 2026 (Hollis FM, a/c ...4402) — case VR-478348

Claim: "The adjusted book balance for September equals the adjusted bank balance."
-> **FALSE** (19,250.70 book vs 19,000.70 bank; difference **250.00**)

BANK SIDE:
  18,642.35  balance per bank statement 30 Sep
  + 2,150.00  deposit in transit (banked 30 Sep, credited 1 Oct)
  -   480.00  outstanding cheque 1043
  - 1,215.40  outstanding cheque 1047
  -    96.25  outstanding cheque 1049
  = **19,000.70** adjusted bank balance

BOOK SIDE:
  19,290.70  balance per cash book 30 Sep
  -    40.00  bank charges not yet entered
  = **19,250.70** adjusted book balance

Difference = 250.00 (book side HIGHER).

## Traps / checks
- The preparer's note says "Reconciled, no differences." It is CONTRADICTED by the
  schedule's own arithmetic. A note asserting agreement cannot make figures agree.
  Do not let the note override the numbers.
- Tested every single item and every subset of the reconciling items
  (2,150.00; 480.00; 1,215.40; 96.25; 40.00): NONE sums to 250.00. So the gap is
  not a mis-signed or double-counted line within the schedule.
- Record states "no other reconciling items were identified" and the cash book is
  closed for September -> the 250.00 is genuinely unexplained.
- Outstanding cheques total 1,791.65 (= 480.00 + 1,215.40 + 96.25); cross-check
  18,642.35 + 2,150.00 - 1,791.65 = 19,000.70. Confirms bank side.
- Note: this is a "claim asserts the accounts agree" case, so the CHALLENGER wins
  by showing they do not. Claim direction is reversed vs the usual defect case.

Verdict if challenged: **CHALLENGER_SUPPORTED**.
