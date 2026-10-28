from typing import Any


def simple_search(
    transactions: list[dict[str, Any]],
    search_query: str,
) -> list[dict[str, Any]]:
    """Ищет операции по описанию или категории."""
    query = search_query.strip().casefold()

    if not query:
        return []

    results = []

    for transaction in transactions:
        description = str(transaction.get("Описание", ""))
        category = str(transaction.get("Категория", ""))

        if query in description.casefold() or query in category.casefold():
            results.append(transaction)

    return results
