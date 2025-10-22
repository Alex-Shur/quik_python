## Основные команды

### Установка и настройка
```bash
# Установить UV (если не установлен)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Инициализация проекта
uv sync

# Установка с dev зависимостями
uv sync --dev
```

### Запуск приложения
```bash
# Через console script
uv run quik-python-demo

# Через модуль
uv run python -m quik_python_demo.main

# Прямой запуск функции
uv run python -c "import quik_python_demo; quik_python_demo.main()"
```

