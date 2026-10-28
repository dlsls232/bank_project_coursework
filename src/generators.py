from collections.abc import Iterator
from typing import Any


def filter_by_currency(
    transactions: list[dict[str, Any]], currency: str
) -> Iterator[dict[str, Any]]:
    for transaction in transactions:
        if transaction["operationAmount"]["currency"]["code"] == currency:
            yield transaction


def transaction_descriptions(
    transactions: list[dict[str, Any]],
) -> Iterator[str]:
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    for number in range(start, end + 1):
        card_number = f"{number:016d}"
        yield " ".join(card_number[i : i + 4] for i in range(0, 16, 4))
