# Bank Project

Проект для работы с банковскими транзакциями.

## Генераторы (`src/generators.py`)

Модуль содержит три генератора:

* `filter_by_currency(transactions, currency)` — возвращает транзакции в указанной валюте.
* `transaction_descriptions(transactions)` — возвращает описания транзакций.
* `card_number_generator(start, end)` — генерирует номера карт в формате `XXXX XXXX XXXX XXXX`.

### Примеры использования

```python
from src.generators import card_number_generator

for card_number in card_number_generator(1, 3):
    print(card_number)
```

Результат:

```text
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
```

## Чтение файлов (`src/reading_files.py`)

Модуль позволяет считывать банковские транзакции из файлов CSV и Excel.

- `read_transactions_from_csv(file_path)` — считывает данные из CSV-файла, в котором значения разделены символом `;`.
- `read_transactions_from_excel(file_path)` — считывает данные из Excel-файла.

Обе функции принимают путь к файлу и возвращают список словарей с данными о транзакциях.


## Тестирование

Запуск тестов:

```bash
poetry run pytest
```

Проверка покрытия кода:

```bash
poetry run pytest --cov=src.generators --cov-report=term-missing --cov-report=html tests
```

HTML-отчёт о покрытии создаётся в папке `htmlcov`.

Тесты генераторов проверяют фильтрацию транзакций по валюте, получение описаний и генерацию номеров карт.
## Поиск и подсчёт операций (`src/search.py`)

- `process_bank_search(data, search)` — ищет операции по тексту в поле `description`. Поиск не зависит от регистра букв.
- `process_bank_operations(data, categories)` — подсчитывает количество операций для каждой указанной категории.

## Запуск программы (`src/main.py`)

Программа позволяет выбрать источник данных: JSON, CSV или Excel. Затем можно отфильтровать операции по статусу, отсортировать их по дате, оставить только операции в рублях и найти операции по описанию.

Для запуска программы используйте команду:

```bash
poetry run python -m src.main
```

## Проверка проекта

Запуск всех тестов:

```bash
poetry run pytest
```

Проверка покрытия кода:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```
