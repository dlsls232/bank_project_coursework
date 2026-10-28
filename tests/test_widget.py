import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("Счет 73654108430135874305", "Счет **4305"),
        ("Visa 7000792289606361", "Visa 7000 79** **** 6361"),
        ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ],
)
def test_mask_account_card(value: str, expected: str) -> None:
    assert mask_account_card(value) == expected


def test_mask_account_card_invalid_value() -> None:
    with pytest.raises(ValueError):
        mask_account_card("Счет")


@pytest.mark.parametrize(
    ("date_string", "expected"),
    [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2025-01-01T00:00:00", "01.01.2025"),
        ("2026-12-31T23:59:59+03:00", "31.12.2026"),
    ],
)
def test_get_date(date_string: str, expected: str) -> None:
    assert get_date(date_string) == expected


def test_get_date_invalid_value() -> None:
    with pytest.raises(ValueError):
        get_date("not-a-date")
