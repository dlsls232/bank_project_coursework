from unittest.mock import patch

import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    ("card_number", "expected"),
    [
        ("7000792289606361", "7000 79** **** 6361"),
        ("1234567890123456", "1234 56** **** 3456"),
        ("12345678", "1234 56** **** 5678"),
    ],
)
def test_get_mask_card_number(card_number: str, expected: str) -> None:
    """Проверяет маскировку номера карты."""
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    ("account_number", "expected"),
    [
        ("73654108430135874305", "**4305"),
        ("1234", "**1234"),
        ("123", "**123"),
    ],
)
def test_get_mask_account(account_number: str, expected: str) -> None:
    """Проверяет маскировку номера счёта."""
    assert get_mask_account(account_number) == expected


def test_get_mask_card_number_logs_success() -> None:
    """Проверяет запись успешной маскировки карты в лог."""
    with patch("src.masks.logger.debug") as mock_debug:
        result = get_mask_card_number("1234567890123456")

    assert result == "1234 56** **** 3456"
    mock_debug.assert_called_once()


def test_get_mask_account_logs_success() -> None:
    """Проверяет запись успешной маскировки счёта в лог."""
    with patch("src.masks.logger.debug") as mock_debug:
        result = get_mask_account("1234567890")

    assert result == "**7890"
    mock_debug.assert_called_once()


def test_get_mask_card_number_logs_and_reraises_error() -> None:
    """Проверяет запись ошибки и повторный вызов исключения."""
    with (
        patch(
            "src.masks.logger.debug",
            side_effect=RuntimeError("Ошибка теста"),
        ),
        patch("src.masks.logger.exception") as mock_exception,
        pytest.raises(RuntimeError, match="Ошибка теста"),
    ):
        get_mask_card_number("1234567890123456")

    mock_exception.assert_called_once()


def test_get_mask_account_logs_and_reraises_error() -> None:
    """Проверяет запись ошибки и повторный вызов исключения."""
    with (
        patch(
            "src.masks.logger.debug",
            side_effect=RuntimeError("Ошибка теста"),
        ),
        patch("src.masks.logger.exception") as mock_exception,
        pytest.raises(RuntimeError, match="Ошибка теста"),
    ):
        get_mask_account("1234567890")

    mock_exception.assert_called_once()
