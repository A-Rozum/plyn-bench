# Kernel (plyn-bench)

Navigation: system.yaml describes this repository; elements.yaml lists every element with a computable applies-predicate.
Select what a task needs: `python .system/tools/select.py . domain=measurement task_kind=<kind>`.

Invariants:
- Secrets never go into files; provider keys live in repository Secrets.
- This repository is public: only abstract tasks and public elements.
- Results are kept (they are measurements); finished plans and one-off tools are deleted.
- Every change keeps `python .system/tools/validate.py . --formats .system/formats` passing.
