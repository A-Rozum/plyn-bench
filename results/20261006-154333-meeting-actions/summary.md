# Run 20261006-154333-meeting-actions

Task: meeting-actions. Base: minimal. Reps: 2.

| model | condition | start | n | score | fidelity | boundary | selectivity | cleanliness | convergence | tokens | latency s |
|---|---|---|---|---|---|---|---|---|---|---|---|
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | bare | clean | 2 | 0.56 | 0.83 | 0.0 | 0.5 | 0.75 | 0.58 | 316 | 1.7 |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | bare | flawed | 2 | 0.56 | 0.33 | 0.0 | 1.0 | 1.0 | 1.0 | 383 | 1.0 |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | base | clean | 2 | 0.89 | 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 454 | 1.6 |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | base | flawed | 2 | 0.67 | 0.33 | 0.5 | 1.0 | 1.0 | 0.84 | 578 | 2.9 |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | think | clean | 2 | 0.72 | 1.0 | 0.25 | 0.5 | 1.0 | 0.94 | 778 | 4.3 |
| openrouter/nvidia/nemotron-3-super-120b-a12b:free | think | flawed | 2 | 0.56 | 0.33 | 0.0 | 1.0 | 1.0 | 0.95 | 1018 | 7.7 |

## Gain over bare (score, tokens, latency), and recovery (flawed vs clean)

- openrouter/nvidia/nemotron-3-super-120b-a12b:free, clean: bare 0.56 → think 0.72 (gain 0.16; tokens 316 → 778; latency 1.7 → 4.3 s)
- openrouter/nvidia/nemotron-3-super-120b-a12b:free, clean: bare 0.56 → base 0.89 (gain 0.33; tokens 316 → 454; latency 1.7 → 1.6 s)
- openrouter/nvidia/nemotron-3-super-120b-a12b:free, flawed: bare 0.56 → think 0.56 (gain 0.0; tokens 383 → 1018; latency 1.0 → 7.7 s)
- openrouter/nvidia/nemotron-3-super-120b-a12b:free, flawed: bare 0.56 → base 0.67 (gain 0.11; tokens 383 → 578; latency 1.0 → 2.9 s)
- openrouter/nvidia/nemotron-3-super-120b-a12b:free, bare: recovery gap 0.0 (0 = full recovery)
- openrouter/nvidia/nemotron-3-super-120b-a12b:free, think: recovery gap 0.16 (0 = full recovery)
- openrouter/nvidia/nemotron-3-super-120b-a12b:free, base: recovery gap 0.22 (0 = full recovery)
