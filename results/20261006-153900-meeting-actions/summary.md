# Run 20261006-153900-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cohere/command-a-03-2025 | bare | clean | 1 | 0.67 | 1.0 | 0.5 | 0.5 | 0.5 | None | 276 | 2.0 |
| cohere/command-a-03-2025 | bare | flawed | 1 | 0.56 | 0.33 | 0.5 | 1.0 | 0.5 | None | 430 | 2.1 |

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- cohere/command-a-03-2025, bare: recovery gap 0.11 (0 = full recovery)
