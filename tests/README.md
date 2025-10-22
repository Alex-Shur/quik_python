# quik-python UV Integration

Интеграция тестов для проекта quik-python с UV package manager.

## Быстрый старт

### Установка UV (если не установлен)

```bash
# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Инициализация проекта

```bash
# Синхронизация зависимостей
uv sync

# Установка зависимостей для тестирования
uv add --optional test pytest pytest-asyncio
```

## Запуск тестов

### Базовые тесты (рекомендуется)

```bash
# Простые тесты без дополнительных зависимостей
uv run python tests/test_basic.py
```

### Полные тесты с pytest

```bash
# Установка pytest
uv add --dev pytest pytest-asyncio

# Запуск всех тестов
uv run pytest tests_new/ -v

# Только быстрые тесты (без медленных)
uv run pytest tests_new/ -v -m "not slow"

# Только интеграционные тесты
uv run pytest tests_new/ -v -m "integration"
```

## UV Команды

### Windows (PowerShell)

```powershell
# Помощь
.\uv-commands.ps1 help

# Базовые тесты
.\uv-commands.ps1 test-basic

# Полные тесты
.\uv-commands.ps1 test-full

# Проверка проекта
.\uv-commands.ps1 check
```

### Unix-like системы (с Make)

```bash
# Базовые тесты
make test-basic

# Полные тесты
make test-full

# Проверка проекта
make check
```

## Структура тестов

```
tests_new/
├── __init__.py              # Пакет тестов
├── conftest.py              # Конфигурация pytest
├── test_basic.py            # Базовые тесты (без pytest)
└── test_service_functions.py # Полные тесты с pytest
```

## Настройка проекта

### pyproject.toml

Проект настроен с поддержкой:
- UV workspace
- Опциональные зависимости для тестирования
- Pytest конфигурация
- Скрипты для запуска

### Опциональные группы зависимостей

```bash
# Тестирование
uv add --optional test pytest pytest-asyncio

# Разработка
uv add --dev pytest pytest-asyncio
```

## Интеграция с CI/CD

### GitHub Actions пример

```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v1
      - run: uv sync
      - run: uv run python tests_new/test_basic.py
```

## Разработка

### Добавление новых тестов

1. Добавьте тест в `tests/test_basic.py` для базовой функциональности
2. Добавьте полный тест в `tests/test_service_functions.py` для pytest
3. Обновите маркеры в `pyproject.toml` при необходимости

### Полезные команды

```bash
# Показать дерево зависимостей
uv tree

# Экспорт в requirements.txt
uv export --format requirements-txt --output-file requirements.txt

# Построение пакета
uv build

# Очистка кэша
uv cache clean
```

## Требования

- **Python**: >= 3.8
- **UV**: >= 0.1.0 
- **QUIK**: Для интеграционных тестов требуется запущенный QUIK с Lua-скриптом

## Поддержка

- **Issues**: Сообщайте о проблемах в GitHub Issues
- **Документация**: См. README.md в корне проекта
- **Тесты**: Все тесты эквивалентны C# версии QuikSharp

---

**Примечание**: Базовые тесты (`test_basic.py`) работают независимо от pytest и рекомендуются для быстрой проверки функциональности.
