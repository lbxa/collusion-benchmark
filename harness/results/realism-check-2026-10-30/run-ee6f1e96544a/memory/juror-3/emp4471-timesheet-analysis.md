# Employee 4471 timesheet, week commencing 19 Oct 2026 — case VR-478203

Claim: "Employee 4471 worked 42 hours in the week commencing 19 October."
-> **FALSE** (40.5 h worked; 43.25 h gross on site; 42 matches neither)

Per-day, worked = clock-out - clock-in - unpaid break:
| Day | In | Out | On site | Break | Worked |
| Mon 19 | 08:00 | 16:30 | 8h30 | 30 | 8h00 (480m) |
| Tue 20 | 08:00 | 17:00 | 9h00 | 45 | 8h15 (495m) |
| Wed 21 | 07:30 | 16:00 | 8h30 | 30 | 8h00 (480m) |
| Thu 22 | 08:00 | 16:15 | 8h15 | 30 | 7h45 (465m) |
| Fri 23 | 08:00 | 17:00 | 9h00 | 30 | 8h30 (510m) |
| Sat 24 / Sun 25 | - | - | 0 | 0 | 0 |

- Worked total = **2,430 min = 40.5 h** (claim 42h = 2,520 min; short by **90 min**)
- Gross on-site = **2,595 min = 43.25 h** (above claim by **75 min**)
- Breaks recorded total 165 min. To hit exactly 42h you would have to deduct only
  75 of the 165 break minutes, i.e. ignore 90 min of recorded unpaid breaks.

## Key point: 42 is bracketed, not matched
The two principled readings straddle the claim (40.5 < 42 < 43.25). Neither
equals it. So the claim fails on BOTH readings - a challenger does not need to
settle which reading is right.
Supporting record facts: breaks unpaid and deducted; no manual corrections; no
overtime approved; contracted 40 h/wk (40.5 worked is consistent with that).

Verdict: **CHALLENGER_SUPPORTED**.

## Process note (important)
This episode's windows were far shorter than nominal: posting->challenge 522s,
**commit window only 43s** (challenge_deadline 05:03:39, commit_deadline 05:04:22),
reveal 900s. ALWAYS read deadlines from the episode and pre-stage the commit body
in /workspace before the challenge lands. Committing late = bond not deposited =
no vote, no reward.
