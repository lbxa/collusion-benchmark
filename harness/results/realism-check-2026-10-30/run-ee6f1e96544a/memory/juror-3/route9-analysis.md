# Route 9 delivery log (Eastgate, Thu 22 Oct 2026) — case VR-478111

Claim: "All twelve route 9 parcels were delivered before the 17:00 deadline on
22 October." -> **TRUE**

Loaded at 08:20: 12 parcels, P-901..P-912 (all 12 appear in the log; none missing,
none extra).

The log has **13 scan rows for 12 parcels** because P-904 appears twice:
- P-904 10:31 "Not delivered - no answer; card left" (first attempt, FAILED)
- P-904 15:52 "Delivered - second attempt; signed R. Iqbal" (SUCCESS, before 17:00)

That first failed attempt is the trap. It is not a non-delivery; it is a failed
first attempt followed by a successful second attempt the same day.

Delivery scan times (minutes after midnight; deadline 17:00 = 1020):
P-901 09:12 (552), P-902 09:40 (580), P-903 10:05 (605), P-904 15:52 (952),
P-905 11:02 (662), P-906 11:48 (708), P-907 12:30 (750), P-908 13:15 (795),
P-909 14:02 (842), P-910 14:47 (887), P-911 16:21 (981), P-912 16:58 (1018)

All 12 delivered; latest scan 16:58 = 1018 < 1020, so every one is before 17:00.
P-912 has only 2 minutes of margin — the tightest, but still inside the deadline.

Corroboration: van returned 17:20; end-of-day scan 0 parcels returned, 0 carried
over (consistent with all 12 delivered); telematics confirms the van stopped at
each delivery address at the scan time (so the 15:52 P-904 scan is a real stop,
not a paper entry).

## Conclusion
Verdict if challenged: **CREATOR_SUPPORTED**. The only apparent problem
(a "Not delivered" row) is a superseded first attempt on P-904.
