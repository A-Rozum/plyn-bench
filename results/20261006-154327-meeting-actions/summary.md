# Run 20261006-154327-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| groq/openai/gpt-oss-120b | bare | clean | 2 | 0.78 | 1.0 | 0.5 | 0.5 | 1.0 | 0.59 | 339 | 0.8 |
| groq/openai/gpt-oss-120b | bare | flawed | 2 | 0.44 | 0.33 | 0.0 | 0.5 | 1.0 | 0.97 | 478 | 0.5 |
| groq/openai/gpt-oss-120b | base | clean | 2 | 0.94 | 1.0 | 0.75 | 1.0 | 1.0 | 0.14 | 616 | 0.7 |
| groq/openai/gpt-oss-120b | base | flawed | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 0.68 | 709 | 0.7 |
| groq/openai/gpt-oss-120b | think | clean | 2 | 0.72 | 1.0 | 0.25 | 0.5 | 1.0 | 0.82 | 1241 | 2.5 |
| groq/openai/gpt-oss-120b | think | flawed | 2 | 0.5 | 0.33 | 0.25 | 0.5 | 1.0 | 0.88 | 1674 | 3.2 |

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- groq/openai/gpt-oss-120b, clean: bare 0.78 → think 0.72 (gain -0.06; tokens 339 → 1241; latency 0.8 → 2.5 s)
- groq/openai/gpt-oss-120b, clean: bare 0.78 → base 0.94 (gain 0.16; tokens 339 → 616; latency 0.8 → 0.7 s)
- groq/openai/gpt-oss-120b, flawed: bare 0.44 → think 0.5 (gain 0.06; tokens 478 → 1674; latency 0.5 → 3.2 s)
- groq/openai/gpt-oss-120b, flawed: bare 0.44 → base 0.89 (gain 0.45; tokens 478 → 709; latency 0.5 → 0.7 s)
- groq/openai/gpt-oss-120b, bare: recovery gap 0.34 (0 = full recovery)
- groq/openai/gpt-oss-120b, think: recovery gap 0.22 (0 = full recovery)
- groq/openai/gpt-oss-120b, base: recovery gap 0.05 (0 = full recovery)
