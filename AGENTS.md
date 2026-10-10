# plyn-bench

Navigation: system.yaml describes this repository; elements.yaml lists every element with a computable applies-predicate.
At the start of a task compile its context and read it instead of browsing: `python .system/tools/plyn_compile.py . domain=measurement task_kind=<kind>` → .context/task.md

Invariants:
- Secrets never go into files; provider keys live in repository Secrets.
- This repository is public: only abstract tasks and public elements.
- Results are kept (they are measurements); finished plans and one-off tools are deleted.
- Service texts (instructions, specifications, manifests, READMEs, commit messages) are in English; drafts and discussion records in A-Rozum/plyn-lab may be in any language.
- Every change keeps `python .system/tools/plyn_validate.py . --formats .system/formats` passing.
