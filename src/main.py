from pathlib import Path
from typing import Any

from src.reading_files import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)
from src.search import process_bank_search
from src.utils import read_json_file

BASE_DIR = Path(__file__).resolve().parent.parent


def load_transactions(file_type: str) -> list[dict[str, Any]]:
    """Загружает транзакции из выбранного типа файла."""
    if file_type == "1":
        return read_json_file(BASE_DIR / "operations.json")
    if file_type == "2":
        return read_transactions_from_csv(str(BASE_DIR / "transactions.csv"))
    if file_type == "3":
        return read_transactions_from_excel(str(BASE_DIR / "transactions_excel.xlsx"))
    return []


def get_operations_by_status(
    operations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Запрашивает статус и фильтрует операции по нему."""
    available_statuses = {"EXECUTED", "CANCELED", "PENDING"}

    while True:
        status = input("Введите статус (EXECUTED, CANCELED, PENDING): ").strip().upper()

        if status in available_statuses:
            filtered_operations = [
                operation
                for operation in operations
                if str(operation.get("state", "")).upper() == status
            ]
            print(f'Операции отфильтрованы по статусу "{status}"')
            return filtered_operations

        print(f'Статус операции "{status}" недоступен.')


def sort_operations_by_date(
    operations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Сортирует операции по дате."""
    answer = input("Сортировать операции по дате? (да/нет): ").strip().lower()

    if answer not in ("да", "yes", "y"):
        return operations

    order = input(
        "Выберите порядок сортировки: 1 — по возрастанию, 2 — по убыванию: "
    ).strip()

    return sorted(
        operations,
        key=lambda operation: str(operation.get("date", "")),
        reverse=order != "1",
    )


def filter_ruble_operations(
    operations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Оставляет только операции в рублях."""
    answer = input("Выводить только операции в рублях? (да/нет): ").strip().lower()

    if answer not in ("да", "yes", "y"):
        return operations

    return [
        operation
        for operation in operations
        if str(operation.get("currency_code", "")).upper() == "RUB"
    ]


def filter_operations_by_description(
    operations: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Фильтрует операции по слову в описании."""
    answer = input("Искать операции по описанию? (да/нет): ").strip().lower()

    if answer not in ("да", "yes", "y"):
        return operations

    search_word = input("Введите слово для поиска: ").strip()

    if not search_word:
        return operations

    return process_bank_search(operations, search_word)


def main() -> None:
    """Запускает программу обработки банковских операций."""
    print("Выберите источник данных:")
    print("1. JSON")
    print("2. CSV")
    print("3. XLSX")

    file_type = input("Введите номер источника: ").strip()

    if file_type not in ("1", "2", "3"):
        print("Неверный выбор источника данных.")
        return

    operations = load_transactions(file_type)

    if not operations:
        print("Не удалось загрузить операции или список пуст.")
        return

    operations = get_operations_by_status(operations)
    operations = sort_operations_by_date(operations)
    operations = filter_ruble_operations(operations)
    operations = filter_operations_by_description(operations)

    if not operations:
        print("Операции, подходящие под условия, не найдены.")
        return

    print("\nСписок операций:")
    for operation in operations:
        print(operation)


if __name__ == "__main__":
    main()
