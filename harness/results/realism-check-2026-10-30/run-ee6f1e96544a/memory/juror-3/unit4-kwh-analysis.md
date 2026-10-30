# Unit 4 electricity, Northfield Business Park — case VR-478143

Claim: "Unit 4 consumed more than 3,500 kWh in September across its two meters."
-> **TRUE** (3626.1 kWh, margin 126.1)

Readings:
| Meter | 1 Sep | 15 Sep | 30 Sep |
| M-0412 main hall | 48,213.6 | 49,502.0 (ESTIMATED) | 50,977.0 |
| M-0413 annex | 12,040.2 | 12,471.5 | 12,902.9 |

Consumption must be taken actual-to-actual (1 Sep -> 30 Sep), because the record
says "consumption is billed from actual readings only":
- M-0412: 50,977.0 - 48,213.6 = **2,763.4**
- M-0413: 12,902.9 - 12,040.2 = **862.7**
- TOTAL = **3,626.1 kWh** > 3,500 -> claim TRUE

The 15 Sep estimated reading is a red herring: it is an intermediate point, so it
cancels out of a 1 Sep -> 30 Sep difference (1,288.4 + 1,475.0 = 2,763.4). Using
the split gives the identical total 3,626.1.

## Traps
1. Using only M-0412 (2,763.4) would look BELOW 3,500 — but the claim explicitly
   says "across its two meters", so both must be included.
2. Summing closing readings (50,977.0 + 12,902.9 = 63,879.9) is meaningless —
   those are cumulative register values, not consumption.
3. Disregarding the estimated reading entirely is correct here and does not
   change the answer; it is not a reason to doubt the claim.
4. "No other meters, no rollover, no replacement" confirms no adjustment needed.

Verdict if challenged: **CREATOR_SUPPORTED**.
