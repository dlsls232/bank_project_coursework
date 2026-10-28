from datetime import datetime
from unittest.mock import patch

from src.reports import spending_by_category


def test_spending_by_category() -> None:
    transactions = [
        {
            "Дата операции": "15.08.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": -100.0,
        },
        {
            "Дата операции": "20.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": -250.0,
        },
        {
            "Дата операции": "10.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Транспорт",
            "Сумма операции": -50.0,
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {"Супермаркеты": 350.0}


def test_ignores_non_ok_transactions() -> None:
    transactions = [
        {
            "Дата операции": "15.09.2021 12:00:00",
            "Статус": "Отклонена",
            "Категория": "Супермаркеты",
            "Сумма операции": -100.0,
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {}


def test_ignores_income() -> None:
    transactions = [
        {
            "Дата операции": "15.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": 100.0,
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {}


def test_ignores_transactions_outside_period() -> None:
    transactions = [
        {
            "Дата операции": "01.06.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": -100.0,
        },
        {
            "Дата операции": "16.10.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": -200.0,
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {}


def test_empty_transactions() -> None:
    assert spending_by_category([], "Супермаркеты", "2021-10-15") == {}


def test_ignores_other_category() -> None:
    transactions = [
        {
            "Дата операции": "15.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Транспорт",
            "Сумма операции": -100.0,
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {}


def test_ignores_zero_amount() -> None:
    transactions = [
        {
            "Дата операции": "15.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": 0,
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {}


def test_ignores_string_amount() -> None:
    transactions = [
        {
            "Дата операции": "15.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": "-100",
        },
    ]

    result = spending_by_category(transactions, "Супермаркеты", "2021-10-15")

    assert result == {}


def test_uses_current_date_when_date_is_none() -> None:
    transactions = [
        {
            "Дата операции": "15.09.2021 12:00:00",
            "Статус": "OK",
            "Категория": "Супермаркеты",
            "Сумма операции": -100.0,
        },
    ]

    with patch("src.reports.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2021, 10, 15)
        mock_datetime.strptime = datetime.strptime

        result = spending_by_category(transactions, "Супермаркеты")

    assert result == {"Супермаркеты": 100.0}
