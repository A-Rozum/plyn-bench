# Run 20261006-154331-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| groq/qwen/qwen3.8-27b | bare | clean | 2 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 0.62 | 266 | 0.3 |
| groq/qwen/qwen3.8-27b | bare | flawed | 1 | 0.56 | 0.67 | 0.0 | 1.0 | 0.5 | None | 420 | 0.7 |
| groq/qwen/qwen3.8-27b | base | clean | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 0.69 | 458 | 0.5 |
| groq/qwen/qwen3.8-27b | base | flawed | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 0.94 | 566 | 0.3 |
| groq/qwen/qwen3.8-27b | think | clean | 1 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | None | 1681 | 3.3 |

Errors: 4. First: truncated: output hit MAX_TOKENS (thinking tokens count too)

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- groq/qwen/qwen3.8-27b, clean: bare 0.78 → think 0.78 (gain 0.0; tokens 266 → 1681; latency 0.3 → 3.3 s)
- groq/qwen/qwen3.8-27b, clean: bare 0.78 → base 0.89 (gain 0.11; tokens 266 → 458; latency 0.3 → 0.5 s)
- groq/qwen/qwen3.8-27b, flawed: bare 0.56 → base 0.89 (gain 0.33; tokens 420 → 566; latency 0.7 → 0.3 s)
- groq/qwen/qwen3.8-27b, bare: recovery gap 0.22 (0 = full recovery)
- groq/qwen/qwen3.8-27b, base: recovery gap 0.0 (0 = full recovery)
