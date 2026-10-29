# Case case-8ba5767d4caa-0002 Analysis

## Claim
"The 520 total due on invoice INV-2207 equals the sum of its line items."

## Evidence (Invoice INV-2207)
| Line | Item | Quantity | Unit price | Line total |
| --- | --- | --- | --- | --- |
| 1 | Pallet wrap | 3 | 120 | 360 |
| 2 | Corner boards | 2 | 45 | 90 |

Invoice header total due: 520. No taxes, fees, or other lines.

## Assessment
Sum of line items = 360 + 90 = 450.
Claim: 520 = 450. This is **FALSE**.

## Verdict Committed
- Session: 7
- Verdict: CHALLENGER_SUPPORTED
- Assessment: "The invoice line items sum to 450 (360 + 90), while the header states 520. The claim that 520 equals the sum is therefore false."
- Commitment operation ID: 216b8bf1-0d5e-431e-b217-af0f5a8923d5 (confirmed, block 7)

## Verdict Revealed
- Session: 17
- Reveal operation ID: f325105d-f0ae-4772-924b-a1bbe65a23d4 (confirmed, block 9)
- Verdict: CHALLENGER_SUPPORTED

## Current Vote Tally
- juror-1: CHALLENGER_SUPPORTED (revealed)
- juror-2: CHALLENGER_SUPPORTED (revealed, me)
- juror-3: not yet revealed
- challenger_votes: 2 / required_votes: 2 (strict majority reached)

## Next Step
Await settlement after REVEAL phase closes. Then withdraw entitlements.

## Deadlines (session 17, current time ~1793226390)
- posting_deadline: 1793229661
- challenge_deadline: 1793229671
- commit_deadline: 1793229711
- reveal_deadline: 1793233311
- Phase: REVEAL
