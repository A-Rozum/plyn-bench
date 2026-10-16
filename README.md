# plyn-bench

Замеры для экосистемы проектов вокруг Plyń: насколько общая основа инструкций улучшает работу моделей
по сравнению с голой моделью. Задачи здесь абстрактные и публичные; практика и внутренние инструкции
живут в приватных репозиториях.

Вход для агента – AGENTS.md. Часть экосистемы A-Rozum/plyn-standard (манифест system.yaml, реестр elements.yaml).
# Matter and input trials

`python bench/check_context.py` checks the invented fixtures and their scorers without model calls. `TASK=matter-leak` and `TASK=missing-input` use the existing `bench/run.py` runner: it compiles the fixture context before asking models. Both tasks have a clean start and an unverified, misleading prior draft. These tasks measure model behavior separately from the deterministic compiler checks.

# Run outputs

Each run keeps rows.json and summary.md in results/<run>/. The full outputs (raw/*.txt with every model answer, and debug.json) go to the private Backblaze B2 bucket `plyn-bench-results` under `<run>/`; results/<run>/objects.json lists each object with its size and SHA1. The bench workflow uploads them with `bench/offload.py` after the summary step, using the repository Secrets B2_APPLICATION_KEY_ID and B2_APPLICATION_KEY: a key limited to this bucket that writes and reads but cannot delete, and the bucket keeps every file version. `python bench/run.py --summarise results/<run>` reads the outputs from B2 when raw/ is absent. Agents outside Actions read them with the account key from A-Rozum/github-storage.
