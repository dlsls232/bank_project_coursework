from calendar import monthrange
from collections import defaultdict
from datetime import datetime
from typing import Any


def spending_by_category(
    transactions: list[dict[str, Any]],
    category: str,
    date: str | None = None,
) -> dict[str, float]:
    """Возвращает расходы по категории за последние три месяца."""

    if date is None:
        end_date = datetime.now()
    else:
        end_date = datetime.strptime(date, "%Y-%m-%d")

    start_month = end_date.month - 3
    start_year = end_date.year

    if start_month <= 0:
        start_month += 12
        start_year -= 1

    start_day = min(
        end_date.day,
        monthrange(start_year, start_month)[1],
    )

    start_date = end_date.replace(
        year=start_year,
        month=start_month,
        day=start_day,
        hour=0,
        minute=0,
        second=0,
    )

    end_date = end_date.replace(
        hour=23,
        minute=59,
        second=59,
    )

    expenses: dict[str, float] = defaultdict(float)

    for transaction in transactions:
        if transaction.get("Статус") != "OK":
            continue

        if transaction.get("Категория") != category:
            continue

        operation_date = datetime.strptime(
            transaction["Дата операции"],
            "%d.%m.%Y %H:%M:%S",
        )

        amount = transaction.get("Сумма операции")

        if (
            start_date <= operation_date <= end_date
            and isinstance(amount, (int, float))
            and not isinstance(amount, bool)
            and amount < 0
        ):
            expenses[category] += abs(float(amount))

    return dict(expenses)
