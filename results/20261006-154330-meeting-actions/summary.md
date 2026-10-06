# Run 20261006-154330-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cohere/command-a-03-2025 | bare | clean | 2 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 1.0 | 263 | 1.8 |
| cohere/command-a-03-2025 | bare | flawed | 2 | 0.56 | 0.33 | 0.5 | 1.0 | 0.5 | 0.85 | 423 | 2.3 |
| cohere/command-a-03-2025 | base | clean | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 450 | 3.3 |
| cohere/command-a-03-2025 | base | flawed | 2 | 0.67 | 0.33 | 0.5 | 1.0 | 1.0 | 1.0 | 575 | 1.9 |

Errors: 4. First: HTTP 400: b'{"id":"d558106c-f106-41f9-a4a3-0f14527dffb7","message":"invalid request: `thinking` parameter is not supported with the specified model."}'

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- cohere/command-a-03-2025, clean: bare 0.78 → base 0.89 (gain 0.11; tokens 263 → 450; latency 1.8 → 3.3 s)
- cohere/command-a-03-2025, flawed: bare 0.56 → base 0.67 (gain 0.11; tokens 423 → 575; latency 2.3 → 1.9 s)
- cohere/command-a-03-2025, bare: recovery gap 0.22 (0 = full recovery)
- cohere/command-a-03-2025, base: recovery gap 0.22 (0 = full recovery)
