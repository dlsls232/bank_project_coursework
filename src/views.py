import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, TypedDict

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_FILE = BASE_DIR / "user_settings.json"


class CategoryAmount(TypedDict):
    category: str
    amount: int


def parse_operation_date(value: Any) -> datetime | None:
    """Преобразует дату операции в datetime."""
    if isinstance(value, datetime):
        return value

    if not isinstance(value, str):
        return None

    try:
        return datetime.strptime(value, "%d.%m.%Y %H:%M:%S")
    except ValueError:
        return None


def get_greeting(date_time: str) -> str:
    """Возвращает приветствие в зависимости от времени суток."""
    hour = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").hour

    if 5 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def load_user_settings() -> dict[str, list[str]]:
    """Загружает пользовательские настройки."""
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
            settings = json.load(file)

        if not isinstance(settings, dict):
            return {"user_currencies": [], "user_stocks": []}

        currencies = settings.get("user_currencies", [])
        stocks = settings.get("user_stocks", [])

        return {
            "user_currencies": (
                [item for item in currencies if isinstance(item, str)]
                if isinstance(currencies, list)
                else []
            ),
            "user_stocks": (
                [item for item in stocks if isinstance(item, str)]
                if isinstance(stocks, list)
                else []
            ),
        }

    except OSError, json.JSONDecodeError:
        return {"user_currencies": [], "user_stocks": []}


def home_page(
    transactions: list[dict[str, Any]],
    date_time: str,
) -> dict[str, Any]:
    """Формирует данные для главной страницы."""
    settings = load_user_settings()

    total_transactions = 0
    total_income = 0.0
    total_expenses = 0.0

    for transaction in transactions:
        if transaction.get("Статус") != "OK":
            continue

        amount = transaction.get("Сумма операции")

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            continue

        total_transactions += 1

        if amount > 0:
            total_income += amount
        elif amount < 0:
            total_expenses += abs(amount)

    return {
        "greeting": get_greeting(date_time),
        "total_transactions": total_transactions,
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "cards": get_cards_data(transactions),
        "top_transactions": get_top_transactions(transactions),
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }


def get_top_transactions(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Возвращает пять самых крупных операций."""
    valid_transactions: list[dict[str, Any]] = []

    for transaction in transactions:
        if transaction.get("Статус") != "OK":
            continue

        amount = transaction.get("Сумма операции")
        date = transaction.get("Дата операции")

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            continue

        if amount == 0:
            continue

        parsed_date = parse_operation_date(date)

        if parsed_date is None:
            continue

        valid_transactions.append(
            {
                "date": parsed_date.strftime("%d.%m.%Y"),
                "amount": abs(amount),
                "category": transaction.get("Категория", ""),
                "description": transaction.get("Описание", ""),
            }
        )

    valid_transactions.sort(
        key=lambda transaction: transaction["amount"],
        reverse=True,
    )

    return valid_transactions[:5]


def get_cards_data(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Возвращает расходы и кэшбэк по картам."""
    cards: dict[str, dict[str, float]] = defaultdict(
        lambda: {"total_spent": 0.0, "cashback": 0.0}
    )

    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        status = transaction.get("Статус")
        amount = transaction.get("Сумма операции")

        if status != "OK":
            continue

        if not isinstance(card_number, str) or not card_number.startswith("*"):
            continue

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            continue

        if amount >= 0:
            continue

        cards[card_number]["total_spent"] += abs(amount)
        cards[card_number]["cashback"] += int(abs(amount) // 100)

    return [
        {
            "last_digits": card_number[-4:],
            "total_spent": round(values["total_spent"], 2),
            "cashback": round(values["cashback"], 2),
        }
        for card_number, values in cards.items()
    ]


def get_currency_rates(
    currencies: list[str],
) -> list[dict[str, Any]]:
    """Получает курсы валют относительно рубля."""
    if not currencies:
        return []

    try:
        response = requests.get(
            "https://open.er-api.com/v6/latest/RUB",
            timeout=5,
        )
        response.raise_for_status()
        rates = response.json().get("rates", {})

        result: list[dict[str, Any]] = []

        for currency in currencies:
            rate = rates.get(currency)

            if isinstance(rate, (int, float)) and rate != 0:
                result.append(
                    {
                        "currency": currency,
                        "rate": round(1 / rate, 2),
                    }
                )

        return result

    except requests.RequestException, ValueError, TypeError:
        return []


def get_stock_prices(stocks: list[str]) -> list[dict[str, Any]]:
    """Получает цены акций."""
    result: list[dict[str, Any]] = []

    for stock in stocks:
        try:
            url = (
                "https://query1.finance.yahoo.com/v8/finance/chart/"
                f"{stock}?range=1d&interval=1d"
            )

            response = requests.get(
                url,
                timeout=5,
                headers={"User-Agent": "Mozilla/5.0"},
            )
            response.raise_for_status()

            data = response.json()
            chart_result = data["chart"]["result"]

            if not chart_result:
                continue

            price = chart_result[0]["meta"].get("regularMarketPrice")

            if isinstance(price, (int, float)) and price > 0:
                result.append(
                    {
                        "stock": stock,
                        "price": round(float(price), 2),
                    }
                )

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            IndexError,
            TypeError,
        ):
            continue

    return result


def events_page(
    transactions: list[dict[str, Any]],
    date_time: str,
    period: str = "M",
) -> dict[str, Any]:
    """Формирует данные для страницы событий."""
    end_date = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")

    if period == "W":
        start_date = (end_date - timedelta(days=end_date.weekday())).replace(
            hour=0, minute=0, second=0
        )

    elif period == "M":
        start_date = end_date.replace(
            day=1,
            hour=0,
            minute=0,
            second=0,
        )

    elif period == "Y":
        start_date = end_date.replace(
            month=1,
            day=1,
            hour=0,
            minute=0,
            second=0,
        )

    elif period == "ALL":
        start_date = datetime.min

    else:
        raise ValueError("Период должен быть W, M, Y или ALL")

    expenses: dict[str, float] = defaultdict(float)
    income: dict[str, float] = defaultdict(float)

    for transaction in transactions:
        if transaction.get("Статус") != "OK":
            continue

        operation_date = parse_operation_date(transaction.get("Дата операции"))

        if operation_date is None:
            continue

        if not start_date <= operation_date <= end_date:
            continue

        amount = transaction.get("Сумма операции")

        if not isinstance(amount, (int, float)) or isinstance(amount, bool):
            continue

        category = transaction.get("Категория", "Без категории")

        if not isinstance(category, str):
            category = "Без категории"

        if amount < 0:
            expenses[category] += abs(amount)
        elif amount > 0:
            income[category] += amount

    transfers_and_cash: list[CategoryAmount] = [
        {
            "category": category,
            "amount": round(expenses[category]),
        }
        for category in ("Наличные", "Переводы")
        if category in expenses
    ]

    transfers_and_cash.sort(
        key=lambda item: item["amount"],
        reverse=True,
    )

    regular_expenses: list[CategoryAmount] = [
        {
            "category": category,
            "amount": round(amount),
        }
        for category, amount in expenses.items()
        if category not in ("Наличные", "Переводы")
    ]

    regular_expenses.sort(
        key=lambda item: item["amount"],
        reverse=True,
    )

    main_expenses = regular_expenses[:7]
    remaining_expenses = regular_expenses[7:]

    if remaining_expenses:
        main_expenses.append(
            {
                "category": "Остальное",
                "amount": sum(item["amount"] for item in remaining_expenses),
            }
        )

    main_income: list[CategoryAmount] = [
        {
            "category": category,
            "amount": round(amount),
        }
        for category, amount in income.items()
    ]

    main_income.sort(
        key=lambda item: item["amount"],
        reverse=True,
    )

    settings = load_user_settings()

    return {
        "expenses": {
            "total_amount": round(sum(expenses.values())),
            "main": main_expenses,
            "transfers_and_cash": transfers_and_cash,
        },
        "income": {
            "total_amount": round(sum(income.values())),
            "main": main_income,
        },
        "currency_rates": get_currency_rates(settings["user_currencies"]),
        "stock_prices": get_stock_prices(settings["user_stocks"]),
    }
