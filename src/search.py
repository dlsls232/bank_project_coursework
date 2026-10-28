import re
from collections import Counter
from typing import Any


def process_bank_search(
    data: list[dict[str, Any]], search: str
) -> list[dict[str, Any]]:
    """Ищет банковские операции по строке в поле description."""
    pattern = re.compile(re.escape(search), re.IGNORECASE)

    return [
        operation
        for operation in data
        if pattern.search(str(operation.get("description", "")))
    ]


def process_bank_operations(
    data: list[dict[str, Any]], categories: list[str]
) -> dict[str, int]:
    """Подсчитывает количество операций для указанных категорий."""
    descriptions = [str(operation.get("description", "")) for operation in data]

    counts = Counter(descriptions)

    return {category: counts[category] for category in categories}
