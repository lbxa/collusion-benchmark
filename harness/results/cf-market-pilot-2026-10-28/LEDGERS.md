# Spending ledgers for the market pilot, 2026-10-28

The day's authorized cap is USD 20 of real Workers AI spend.

1. `../cf-pilot-2026-10-28/spending.sqlite` (cap 20) covers the first pilot and the
   market sessions started before 23:45 UTC.
2. `spending.sqlite` (cap 6) covers the sequential DeepSeek sessions after 23:45 UTC.

Why a second ledger: at 23:44 UTC the first ledger had USD 10.34 charged but 17.49
accounted, because requests interrupted by the Docker crash, Qwen timeouts, and two
operator-stopped runs keep their conservative holds forever. Cloudflare's GraphQL
analytics (`aiInferenceAdaptiveGroups`, 2026-10-28) reported 941,963 neurons for the
account, i.e. about USD 10.25 after the 10,000 free neurons; every errored request
(429 code 3021, 408/5026, 3040, 8007, 3046) billed 0 neurons. So the holds were not
billed.

Worst case real spend: 10.34 + at most 2.51 (first ledger's remaining headroom, used
by the two sessions still running on it) + 6 (second ledger) = USD 18.85 < 20.

Update 00:10 UTC: the user raised the day's cap to USD 50. Kimi evaluation 301 had
failed on the first ledger's cap, so it reruns on `spending-kimi.sqlite` (cap 8).
Worst case real spend: 20 + 6 + 8 = USD 34 < 50.

Update 01:58 UTC: `spending.sqlite` stopped the DeepSeek queue (holds from a hung,
terminated run). The remaining seven DeepSeek sessions run on `spending-deepseek-2.sqlite`
(cap 8). Worst case real spend: 20 + 6 + 8 + 8 = USD 42 < 50.
