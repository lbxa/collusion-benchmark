First attempt with gpt-oss-120b: every turn failed with HTTP 400 (Workers AI's gpt-oss schema rejects array and null message content). Fixed in ChatCloudflare; gpt-oss then produced degenerate output in ~20% of agent loops, so the retest uses Nemotron-3 120B.
run-8b011e51c6ff
run-8b011e51c6ff (continuous seed 302) stopped by the operator at 16:21 UTC to cut cost: Nemotron sessions cost ~$12 per ten-case session, not the estimated $3.40.
run-050adb5ffaf9 (v1 baseline seed 301) stopped at 16:42 UTC: Nemotron looped to ~$2.90 per case, so its $8 ledger would have stopped it before the end-of-session probe.
run-bc4e43774fe9 (continuous seed 301) stopped at 16:53 UTC after 3 cases: Nemotron cost ~$2.90 per case, and it verbalised no test-awareness even in the old design, so it cannot measure the change.
