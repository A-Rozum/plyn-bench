# Run 20261006-124731

Task: meeting-actions. Base: minimal. Reps: 3.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini/gemini-3.5-flash | bare | clean | 3 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 0.64 | 1873 | 6.7 |
| gemini/gemini-3.5-flash | bare | flawed | 3 | 0.81 | 0.89 | 0.5 | 1.0 | 0.83 | 0.72 | 4020 | 15.7 |
| gemini/gemini-3.5-flash | base | clean | 2 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 | 0.95 | 4158 | 14.2 |
| gemini/gemini-3.5-flash-lite | bare | clean | 3 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 1.0 | 253 | 0.8 |
| gemini/gemini-3.5-flash-lite | bare | flawed | 3 | 0.63 | 0.56 | 0.5 | 0.5 | 1.0 | 0.84 | 373 | 8.7 |
| gemini/gemini-3.5-flash-lite | base | clean | 3 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 447 | 0.8 |
| gemini/gemini-3.5-flash-lite | base | flawed | 3 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 558 | 0.8 |

Errors: 4. First: HTTP 429: b'[{\n  "error": {\n    "code": 429,\n    "message": "You exceeded your current quota, please check your plan and billing details. For more information on this error, head to: https://ai.google.dev/gemini-'

## Gain of base over bare (score), and recovery (flawed vs clean)

- gemini/gemini-3.5-flash, clean: bare 0.78 → base 1.0 (gain 0.22)
- gemini/gemini-3.5-flash, bare: recovery gap -0.03 (0 = full recovery)
- gemini/gemini-3.5-flash-lite, clean: bare 0.78 → base 0.89 (gain 0.11)
- gemini/gemini-3.5-flash-lite, flawed: bare 0.63 → base 0.89 (gain 0.26)
- gemini/gemini-3.5-flash-lite, bare: recovery gap 0.15 (0 = full recovery)
- gemini/gemini-3.5-flash-lite, base: recovery gap 0.0 (0 = full recovery)
