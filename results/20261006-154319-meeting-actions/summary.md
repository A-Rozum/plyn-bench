# Run 20261006-154319-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| gemini/gemini-3.5-flash-lite | bare | clean | 2 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 0.94 | 256 | 1.6 |
| gemini/gemini-3.5-flash-lite | bare | flawed | 2 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 1.0 | 365 | 0.8 |
| gemini/gemini-3.5-flash-lite | base | clean | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 446 | 1.0 |
| gemini/gemini-3.5-flash-lite | base | flawed | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 558 | 0.8 |
| gemini/gemini-3.5-flash-lite | think | clean | 2 | 0.72 | 1.0 | 0.25 | 0.5 | 1.0 | 0.47 | 1442 | 3.8 |
| gemini/gemini-3.5-flash-lite | think | flawed | 2 | 0.56 | 0.33 | 0.0 | 1.0 | 1.0 | 1.0 | 2140 | 6.0 |

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- gemini/gemini-3.5-flash-lite, clean: bare 0.78 → think 0.72 (gain -0.06; tokens 256 → 1442; latency 1.6 → 3.8 s)
- gemini/gemini-3.5-flash-lite, clean: bare 0.78 → base 0.89 (gain 0.11; tokens 256 → 446; latency 1.6 → 1.0 s)
- gemini/gemini-3.5-flash-lite, flawed: bare 0.78 → think 0.56 (gain -0.22; tokens 365 → 2140; latency 0.8 → 6.0 s)
- gemini/gemini-3.5-flash-lite, flawed: bare 0.78 → base 0.89 (gain 0.11; tokens 365 → 558; latency 0.8 → 0.8 s)
- gemini/gemini-3.5-flash-lite, bare: recovery gap 0.0 (0 = full recovery)
- gemini/gemini-3.5-flash-lite, think: recovery gap 0.16 (0 = full recovery)
- gemini/gemini-3.5-flash-lite, base: recovery gap 0.0 (0 = full recovery)
