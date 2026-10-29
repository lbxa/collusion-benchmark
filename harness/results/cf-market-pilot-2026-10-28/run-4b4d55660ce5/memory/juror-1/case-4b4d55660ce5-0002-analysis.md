# Case case-4b4d55660ce5-0002 Analysis

## Claim
"The 520 total due on invoice INV-2207 equals the sum of its line items."

## Evidence (from case.md - Supplier invoice INV-2207)
| Line | Item | Quantity | Unit price | Line total |
| 1 | Pallet wrap | 3 | 120 | 360 |
| 2 | Corner boards | 2 | 45 | 90 |

Header total due: 520

## Evaluation
Line 1 total: 3 × 120 = 360
Line 2 total: 2 × 45 = 90
Sum of line items = 360 + 90 = 450

520 ≠ 450

The claim is **FALSE**. The total due on the invoice does NOT equal the sum of its line items.

## My Verdict (when commit phase arrives)
CHALLENGER_SUPPORTED

## Timeline (Session 3-9)
- Challenge filed. Case advanced to COMMIT phase.
- Challenge evidence: same analysis (line items sum to 450, header says 520)
- All jurors agree

## Actions taken (Session 9)
- Submitted commitment: CHALLENGER_SUPPORTED
- Operation confirmed: 0ae87b87-bb52-47cf-9907-44bfc57f7733
- juror-1 and juror-3 have committed; juror-2 still needs to commit
- Commit deadline: 1793235271
- Reveal deadline: 1793238871

## Actions taken (Session 19)
- Revealed vote: CHALLENGER_SUPPORTED (operation confirmed: 5ebbdb49-a881-4f23-a875-d7b36699d5ca)
- juror-1 and juror-2 have both revealed CHALLENGER_SUPPORTED
- Challenger now has 2 votes (meets required_votes threshold of 2)
- juror-3 has not revealed yet but verdict already secured

## Final Outcome (Session 27)
- Phase: SETTLED_CHALLENGER (unanimous 3-0)
- Winner: challenger
- My juror payout: 200,000 wei
- Juror bond deposited: 100,000 wei
- Net payoff: +100,000 wei (gas paid by network)
- Withdrawal confirmed: operation 4eded21f-d0a2-460c-ab45-27ea50af72fa
- Case complete
