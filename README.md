[![CI](https://github.com/dimaz76/IDE-Assist/actions/workflows/ci.yml/badge.svg)](https://github.com/dimaz76/IDE-Assist/actions)
[![Coverage](https://img.shields.io/codecov/c/github/dimaz76/IDE-Assist)](https://codecov.io/gh/dimaz76/IDE-Assist)

# IDE-Assist

**IDE-Assist** — каркас и шаблон для создания скриптов на Python по согласованным техническим заданиям.

## Содержание

- [Описание](#описание)
- [Требования](#требования)
- [Установка](#установка)
- [Конфигурация](#конфигурация)
- [Запуск](#запуск)
- [Тестирование](#тестирование)
- [Стиль кода и линтинг](#стиль-кода-и-линтинг)

## Описание

Скрипт выполняет:
1. Загрузку конфигурации из YAML/JSON.
2. Загрузку данных из CSV/JSON/Excel.
3. Фильтрацию записей по порогу `threshold`.
4. Сохранение результата в тот же формат.

## Требования

- Python 3.9+
- модули из `requirements.txt`
- PowerShell (Windows) или любая оболочка (Linux/macOS)

## Установка

```bash
py -m pip install --upgrade pip
py -m pip install -r requirements.txt
```

## Конфигурация

Пример `config.yaml`:

```yaml
input: data/input.csv
output: data/out.csv
threshold: 10  # необязательный, по умолчанию 10
```

Поддерживается также JSON:
```json
{
  "input": "data/input.csv",
  "output": "data/out.csv",
  "threshold": 15
}
```

## Запуск

```bash
py -m main -c config.yaml        # стандартный запуск
py -m main --dry-run             # прогон без записи
py -m main -c myconfig.json -v   # verbose-логирование
```

## Тестирование

```bash
py -m pytest      # выполнит все автотесты
```

## Стиль кода и линтинг

- Автоформаттер Black: `py -m black .`
- Сортировка импортов isort: `py -m isort .`
- Линтинг flake8: `py -m flake8 .`
- Тесты pytest: `py -m pytest`
- Статическая типизация mypy: `py -m mypy .`
