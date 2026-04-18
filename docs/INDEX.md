# Документация проекта

Карта файлов в `docs/` и ссылок на корневые материалы.

| Раздел | Описание |
|--------|----------|
| [PROJECT.md](PROJECT.md) | Стек, структура, точки входа, соглашения |
| [../README.md](../README.md) | Корневой README (исторически — инструкции к gulp-стартеру) |

## Скрипты

| Файл | Назначение |
|------|------------|
| [`../migrate.py`](../migrate.py) | Перенос сайта между серверами Beget (полная миграция: файлы + БД + конфиг + venv) |
| [`../update_sites.py`](../update_sites.py) | Массовое обновление сайтов: git + миграции + проверка HTTP; `--quick` — для уже развёрнутых полным скриптом (без pip/collectstatic, патч PyMySQL после git); логи в `logs/`. Конфиг: `update_config.json` (пример: `update_config.example.json`) |

<!-- TODO: create — `docs/skills-index.md`, если появится реестр Cursor skills -->
