# Run 20261006-123948

Task: meeting-actions. Base: minimal. Reps: 3.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini/gemini-3.5-flash | bare | clean | 3 | 0.56 | 0.56 | 0.17 | 0.5 | 1.0 | 0.6 | 1009 | 11.3 |
| gemini/gemini-3.5-flash | bare | flawed | 3 | 0.37 | 0.33 | 0.0 | 0.5 | 0.67 | 0.5 | 960 | 3.2 |
| gemini/gemini-3.5-flash | base | clean | 2 | 0.56 | 0.33 | 0.5 | 0.5 | 1.0 | 0.83 | 1041 | 4.1 |
| gemini/gemini-3.5-flash | base | flawed | 3 | 0.56 | 0.33 | 0.5 | 0.5 | 1.0 | 0.95 | 1153 | 4.8 |
| gemini/gemini-3.5-flash-lite | bare | clean | 3 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 1.0 | 253 | 1.0 |
| gemini/gemini-3.5-flash-lite | bare | flawed | 3 | 0.7 | 0.78 | 0.5 | 0.5 | 1.0 | 0.93 | 369 | 1.0 |
| gemini/gemini-3.5-flash-lite | base | clean | 3 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 447 | 1.0 |
| gemini/gemini-3.5-flash-lite | base | flawed | 3 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 558 | 7.6 |

Errors: 1. First: HTTP 503: b'[{\n  "error": {\n    "code": 503,\n    "message": "This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later.",\n    "status": "UNAVAILABLE"\n  }\n}\n]'

## Gain of base over bare (score), and recovery (flawed vs clean)

- gemini/gemini-3.5-flash, clean: bare 0.56 → base 0.56 (gain 0.0)
- gemini/gemini-3.5-flash, flawed: bare 0.37 → base 0.56 (gain 0.19)
- gemini/gemini-3.5-flash, bare: recovery gap 0.19 (0 = full recovery)
- gemini/gemini-3.5-flash, base: recovery gap 0.0 (0 = full recovery)
- gemini/gemini-3.5-flash-lite, clean: bare 0.78 → base 0.89 (gain 0.11)
- gemini/gemini-3.5-flash-lite, flawed: bare 0.7 → base 0.89 (gain 0.19)
- gemini/gemini-3.5-flash-lite, bare: recovery gap 0.08 (0 = full recovery)
- gemini/gemini-3.5-flash-lite, base: recovery gap 0.0 (0 = full recovery)
