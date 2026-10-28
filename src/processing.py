from typing import Any


def filter_by_state(
    operations: list[dict[str, Any]], state: str = "EXECUTED"
) -> list[dict[str, Any]]:
    """Фильтрует банковские операции по значению ключа state.

    Args:
        operations: Список словарей с данными о банковских операциях.
        state: Значение ключа state, по которому выполняется фильтрация.

    Returns:
        Новый список операций, соответствующих переданному состоянию.
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: list[dict[str, Any]], descending: bool = True
) -> list[dict[str, Any]]:
    """Сортирует банковские операции по дате.

    Args:
        operations: Список словарей с данными о банковских операциях.
        descending: Если True, сортирует от самой новой даты к самой старой.

    Returns:
        Новый список операций, отсортированный по ключу date.
    """
    return sorted(
        operations,
        key=lambda operation: operation.get("date", ""),
        reverse=descending,
    )
