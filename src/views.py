import json
import math
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any

import requests

BASE_DIR = Path(__file__).resolve().parent.parent
SETTINGS_FILE = BASE_DIR / "user_settings.json"


def get_greeting(date_time: str) -> str:
    """Возвращает приветствие в зависимости от времени."""
    operation_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
    hour = operation_time.hour

    if 6 <= hour < 12:
        return "Доброе утро"
    if 12 <= hour < 18:
        return "Добрый день"
    if 18 <= hour < 23:
        return "Добрый вечер"
    return "Доброй ночи"


def load_user_settings() -> dict[str, list[str]]:
    """Загружает настройки валют и акций из JSON-файла."""
    try:
        with SETTINGS_FILE.open("r", encoding="utf-8") as file:
            settings = json.load(file)

        if not isinstance(settings, dict):
            return {"user_currencies": [], "user_stocks": []}

        currencies = settings.get("user_currencies", [])
        stocks = settings.get("user_stocks", [])

        return {
            "user_currencies": (
                currencies
                if isinstance(currencies, list)
                and all(isinstance(item, str) for item in currencies)
                else []
            ),
            "user_stocks": (
                stocks
                if isinstance(stocks, list)
                and all(isinstance(item, str) for item in stocks)
                else []
            ),
        }
    except OSError, json.JSONDecodeError:
        return {"user_currencies": [], "user_stocks": []}


def home_page(
    transactions: list[dict[str, Any]],
    date_time: str,
) -> dict[str, Any]:
    """Подготавливает данные для главной страницы."""
    total_income = sum(
        float(transaction["Сумма операции"])
        for transaction in transactions
        if transaction.get("Статус") == "OK"
        and isinstance(transaction.get("Сумма операции"), (int, float))
        and math.isfinite(transaction["Сумма операции"])
        and transaction["Сумма операции"] > 0
    )

    total_expenses = sum(
        abs(float(transaction["Сумма операции"]))
        for transaction in transactions
        if transaction.get("Статус") == "OK"
        and isinstance(transaction.get("Сумма операции"), (int, float))
        and math.isfinite(transaction["Сумма операции"])
        and transaction["Сумма операции"] < 0
    )

    settings = load_user_settings()

    return {
        "greeting": get_greeting(date_time),
        "total_transactions": len(transactions),
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
    """Возвращает пять крупнейших операций."""
    valid_transactions = [
        transaction
        for transaction in transactions
        if transaction.get("Статус") == "OK"
        and isinstance(transaction.get("Сумма операции"), (int, float))
        and math.isfinite(transaction["Сумма операции"])
        and isinstance(transaction.get("Дата операции"), str)
    ]

    top_transactions = sorted(
        valid_transactions,
        key=lambda transaction: abs(transaction["Сумма операции"]),
        reverse=True,
    )[:5]

    result = []

    for transaction in top_transactions:
        try:
            operation_date = datetime.strptime(
                transaction["Дата операции"],
                "%d.%m.%Y %H:%M:%S",
            ).strftime("%d.%m.%Y")
        except ValueError:
            continue

        result.append(
            {
                "date": operation_date,
                "amount": abs(transaction["Сумма операции"]),
                "category": transaction.get("Категория", ""),
                "description": transaction.get("Описание", ""),
            }
        )

    return result


def get_cards_data(
    transactions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Возвращает расходы и кэшбэк по каждой карте."""
    cards: dict[str, dict[str, float]] = defaultdict(
        lambda: {"total_spent": 0.0, "cashback": 0.0}
    )

    for transaction in transactions:
        card_number = transaction.get("Номер карты")
        amount = transaction.get("Сумма операции", 0)

        if not isinstance(card_number, str) or not card_number.startswith("*"):
            continue

        if transaction.get("Статус") != "OK":
            continue

        if not isinstance(amount, (int, float)) or not math.isfinite(amount):
            continue

        if amount < 0:
            spent = abs(float(amount))
            cards[card_number]["total_spent"] += spent
            cards[card_number]["cashback"] += math.floor(spent / 100)

    return [
        {
            "last_digits": card[-4:],
            "total_spent": round(values["total_spent"], 2),
            "cashback": round(values["cashback"], 2),
        }
        for card, values in sorted(cards.items())
    ]


def get_currency_rates(
    currencies: list[str],
) -> list[dict[str, Any]]:
    """Получает курсы валют в рублях за одну единицу валюты."""
    try:
        response = requests.get(
            "https://open.er-api.com/v6/latest/RUB",
            timeout=10,
        )
        response.raise_for_status()
        rates = response.json().get("rates", {})
    except requests.RequestException, ValueError, AttributeError:
        return []

    result = []

    for currency in currencies:
        rate = rates.get(currency)

        if isinstance(rate, (int, float)) and rate > 0:
            result.append(
                {
                    "currency": currency,
                    "rate": round(1 / rate, 4),
                }
            )

    return result


def get_stock_prices(
    stocks: list[str],
) -> list[dict[str, Any]]:
    """Получает текущие цены акций через Yahoo Finance."""
    result = []

    for stock in stocks:
        try:
            response = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{stock}",
                headers={"User-Agent": "Mozilla/5.0"},
                timeout=10,
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
                        "price": float(price),
                    }
                )

        except (
            requests.RequestException,
            ValueError,
            KeyError,
            TypeError,
        ):
            continue

    return result
