# plyn-bench

Замеры для экосистемы проектов вокруг Plyń: насколько общая основа инструкций улучшает работу моделей
по сравнению с голой моделью. Задачи здесь абстрактные и публичные; практика и внутренние инструкции
живут в приватных репозиториях.

Вход для агента – AGENTS.md. Часть экосистемы A-Rozum/system (манифест system.yaml, реестр elements.yaml).
# Matter and input trials

`python bench/check_context.py` checks the invented fixtures and their scorers without model calls. `TASK=matter-leak` and `TASK=missing-input` use the existing `bench/run.py` runner: it compiles the fixture context before asking models. Both tasks have a clean start and an unverified, misleading prior draft. These tasks measure model behavior separately from the deterministic compiler checks.
