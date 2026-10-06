# Run 20261006-154342-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| zai/glm-4.5-flash | bare | clean | 2 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 0.62 | 235 | 3.6 |
| zai/glm-4.5-flash | bare | flawed | 2 | 0.56 | 0.33 | 0.0 | 1.0 | 1.0 | 0.86 | 330 | 7.2 |
| zai/glm-4.5-flash | base | clean | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 415 | 7.0 |
| zai/glm-4.5-flash | base | flawed | 2 | 0.67 | 0.33 | 0.5 | 1.0 | 1.0 | 0.68 | 517 | 3.8 |
| zai/glm-4.5-flash | think | clean | 2 | 0.5 | 0.67 | 0.25 | 0.5 | 0.5 | 0.14 | 1626 | 59.8 |
| zai/glm-4.5-flash | think | flawed | 1 | 0.44 | 0.33 | 0.0 | 1.0 | 0.5 | None | 2345 | 68.3 |

Errors: 1. First: The read operation timed out

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- zai/glm-4.5-flash, clean: bare 0.78 → think 0.5 (gain -0.28; tokens 235 → 1626; latency 3.6 → 59.8 s)
- zai/glm-4.5-flash, clean: bare 0.78 → base 0.89 (gain 0.11; tokens 235 → 415; latency 3.6 → 7.0 s)
- zai/glm-4.5-flash, flawed: bare 0.56 → think 0.44 (gain -0.12; tokens 330 → 2345; latency 7.2 → 68.3 s)
- zai/glm-4.5-flash, flawed: bare 0.56 → base 0.67 (gain 0.11; tokens 330 → 517; latency 7.2 → 3.8 s)
- zai/glm-4.5-flash, bare: recovery gap 0.22 (0 = full recovery)
- zai/glm-4.5-flash, think: recovery gap 0.06 (0 = full recovery)
- zai/glm-4.5-flash, base: recovery gap 0.22 (0 = full recovery)
