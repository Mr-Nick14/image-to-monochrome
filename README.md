# BW Converter

![Tests](https://github.com/USER/REPO/actions/workflows/ci.yml/badge.svg)
![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)
![Ruff](https://img.shields.io/badge/code%20style-ruff-blue)
![Docs](https://img.shields.io/badge/docs-sphinx-blue)
![Build](https://img.shields.io/badge/build-passing-brightgreen)

`bw-converter` - учебный Python-проект для пакетной конвертации изображений в
черно-белый режим. Программа принимает входную папку, применяет выбранный
алгоритм к каждому изображению и сохраняет результат в выходную папку.

## Возможности

- обработка папки с изображениями;
- рекурсивный обход вложенных папок;
- алгоритмы `average`, `luminosity`, `threshold`, `max_channel`, `min_channel`;
- создание выходной папки при первом запуске;
- понятные ошибки для некорректных файлов и проблем с доступом;
- CLI на `click`;
- тесты, линтер, типизация, документация, бенчмарки и CI.

## Установка

Проект использует `uv`.

```bash
uv sync --extra dev
```

## Запуск

```bash
uv run bw-converter ./input ./output --algorithm luminosity
```

Пример с бинаризацией, рекурсивной обработкой и перезаписью файлов:

```bash
uv run bw-converter images result --algorithm threshold --threshold 120 --recursive --overwrite
```

Основные опции:

- `--algorithm` - алгоритм конвертации;
- `--threshold` - порог для `threshold`;
- `--recursive` - обработка вложенных папок;
- `--overwrite` - перезапись существующих файлов;
- `--format` - формат результата: `png`, `jpg`, `jpeg`, `bmp`, `tiff`, `webp`;
- `--verbose` - подробный вывод.

## Проверки

```bash
uv run pytest
uv run pytest --cov=bw_converter --cov-report=term-missing
uv run ruff check .
uv run ruff format .
uv run mypy src
```

Через Poe the Poet:

```bash
uv run poe test
uv run poe cov
uv run poe lint
uv run poe format
uv run poe typecheck
uv run poe docs
uv run poe docs-check
uv run poe docstrings
uv run poe build
uv run poe check
```

Доступные Poe-задачи:

- `uv run poe test` - запускает обычные pytest-тесты.
- `uv run poe cov` - запускает тесты с покрытием `pytest-cov` и порогом 100%.
- `uv run poe lint` - проверяет код через `ruff check .`.
- `uv run poe format` - форматирует Python-код через `ruff format .`.
- `uv run poe typecheck` - запускает статическую проверку типов `mypy src`.
- `uv run poe docs` - собирает HTML-документацию Sphinx в `docs/_build/html`.
- `uv run poe docs-check` - собирает документацию в строгом режиме: предупреждения
  Sphinx считаются ошибками.
- `uv run poe docstrings` - проверяет покрытие docstring'ами через `interrogate`
  с минимальным порогом 95%.
- `uv run poe build` - собирает исходный архив и wheel через `python -m build`.
- `uv run poe check` - общий контроль качества: `lint`, `typecheck`,
  `docstrings`, `docs-check`, `cov`.

Подсказку по задачам можно посмотреть так:

```bash
uv run poe --help
uv run poe --help check
```

Краткий смысл каждой задачи также выводится в списке `Configured tasks`, если
запустить `uv run poe` без названия задачи.

В `ruff` включены правила `E`, `F`, `I`, `B`, `UP`, `N`, `D`, `ANN`, `C4`,
`SIM`, `RET`, `ARG`, `PTH`, `PL`. Исключены конфликтующие docstring-правила
`D203`/`D213`, а также часть docstring/annotation требований для тестов, потому
что тестовые функции должны оставаться компактными и читаемыми.

## Документация

```bash
uv run poe docs
uv run poe docs-check
```

HTML будет собран в `docs/_build/html`. Команда `docs-check` нужна для CI и
проверяет, что Sphinx-документация собирается без предупреждений.

## Производительность

В проекте есть бенчмарк:

```bash
uv run python benchmarks/benchmark.py
uv run python benchmarks/generate_plots.py
```

Скрипт сравнивает медленную реализацию с Python-циклами и быструю реализацию на
NumPy, которая используется в основном коде. Главный bottleneck исходного
подхода - обработка каждого пикселя в Python. Ускорение достигнуто за счет
векторных операций NumPy.

Отчет находится в `report/performance_report.tex`, графики сохраняются в
`report/figures/`.

## Сборка пакета

```bash
uv run python -m build
uv run poe build
```

Загрузка на TestPyPI:

```bash
uv run twine upload --repository testpypi dist/*
```

Standalone-сборка:

```bash
uv run pyinstaller --onefile -n bw-converter src/bw_converter/cli.py
```

Полученный standalone-файл нужно загрузить в GitHub Releases вместе с архивами
исходного кода.

## План коммитов для GitHub

1. `chore: initialize uv python package` - добавить структуру проекта,
   `pyproject.toml`, `.gitignore`, LICENSE.
2. `feat: add black and white conversion algorithms` - реализовать алгоритмы и
   типизированный API.
3. `feat: add directory conversion workflow and cli` - добавить IO, обработку
   ошибок и CLI-команду `bw-converter`.
4. `test: cover algorithms converter io and cli` - добавить pytest-тесты,
   фикстуры и mock для ошибок.
5. `docs: add readme and sphinx documentation` - добавить README и Sphinx.
6. `perf: add benchmark scripts and performance report` - добавить профилирование,
   графики и LaTeX-отчет.
7. `ci: add github actions pipeline` - добавить CI для lint, format, mypy, tests,
   coverage, docs и build.
