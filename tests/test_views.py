from typing import Any

from src.views import (
    get_cards_data,
    get_greeting,
    get_top_transactions,
    home_page,
    load_user_settings,
)


def test_get_greeting() -> None:
    assert get_greeting("2025-01-01 08:00:00") == "Доброе утро"
    assert get_greeting("2025-01-01 14:00:00") == "Добрый день"
    assert get_greeting("2025-01-01 20:00:00") == "Добрый вечер"
    assert get_greeting("2025-01-01 02:00:00") == "Доброй ночи"


def test_get_cards_data() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "Номер карты": "*1234",
            "Статус": "OK",
            "Сумма операции": -250.0,
        },
        {
            "Номер карты": "*1234",
            "Статус": "OK",
            "Сумма операции": -150.0,
        },
        {
            "Номер карты": "*5678",
            "Статус": "OK",
            "Сумма операции": 500.0,
        },
    ]

    result = get_cards_data(transactions)

    assert result == [
        {"last_digits": "1234", "total_spent": 400.0, "cashback": 3.0},
    ]


def test_get_cards_data_ignores_invalid_transactions() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "Номер карты": "*1234",
            "Статус": "Отклонена",
            "Сумма операции": -100.0,
        },
        {
            "Номер карты": "1234",
            "Статус": "OK",
            "Сумма операции": -100.0,
        },
        {
            "Номер карты": "*5678",
            "Статус": "OK",
            "Сумма операции": "100",
        },
    ]

    assert get_cards_data(transactions) == []


def test_get_top_transactions() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "Дата операции": "15.01.2025 12:00:00",
            "Статус": "OK",
            "Сумма операции": -100.0,
            "Категория": "Продукты",
            "Описание": "Магазин",
        },
        {
            "Дата операции": "16.01.2025 12:00:00",
            "Статус": "OK",
            "Сумма операции": 500.0,
            "Категория": "Пополнение",
            "Описание": "Зарплата",
        },
        {
            "Дата операции": "17.01.2025 12:00:00",
            "Статус": "Отклонена",
            "Сумма операции": -900.0,
            "Категория": "Продукты",
            "Описание": "Отклонённая операция",
        },
    ]

    result = get_top_transactions(transactions)

    assert len(result) == 2
    assert result[0]["amount"] == 500.0
    assert result[1]["amount"] == 100.0
    assert result[1]["date"] == "15.01.2025"


def test_get_top_transactions_limits_to_five() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "Дата операции": f"{day:02d}.01.2025 12:00:00",
            "Статус": "OK",
            "Сумма операции": -float(day * 100),
            "Категория": "Покупки",
            "Описание": f"Операция {day}",
        }
        for day in range(1, 8)
    ]

    result = get_top_transactions(transactions)

    assert len(result) == 5
    assert result[0]["amount"] == 700.0
    assert result[-1]["amount"] == 300.0


def test_get_top_transactions_invalid_date() -> None:
    transactions: list[dict[str, Any]] = [
        {
            "Дата операции": "неверная дата",
            "Статус": "OK",
            "Сумма операции": -100.0,
        }
    ]

    assert get_top_transactions(transactions) == []


def test_load_user_settings() -> None:
    settings = load_user_settings()

    assert "user_currencies" in settings
    assert "user_stocks" in settings
    assert isinstance(settings["user_currencies"], list)
    assert isinstance(settings["user_stocks"], list)


def test_home_page_without_transactions() -> None:
    result = home_page([], "2025-01-01 14:00:00")

    assert result["greeting"] == "Добрый день"
    assert result["total_transactions"] == 0
    assert result["total_income"] == 0
    assert result["total_expenses"] == 0
    assert result["cards"] == []
    assert result["top_transactions"] == []
    assert isinstance(result["currency_rates"], list)
    assert isinstance(result["stock_prices"], list)
