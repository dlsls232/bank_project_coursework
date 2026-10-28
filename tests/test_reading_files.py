from unittest.mock import Mock, patch

import pandas as pd

from src.reading_files import (
    read_transactions_from_csv,
    read_transactions_from_excel,
)


@patch("src.reading_files.pd.read_csv")
def test_read_transactions_from_csv(mock_read_csv: Mock) -> None:
    """Проверяет чтение операций из CSV-файла."""
    mock_read_csv.return_value = pd.DataFrame(
        [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    )

    result = read_transactions_from_csv("test.csv")

    assert len(result) == 2
    assert result[0]["amount"] == 100
    mock_read_csv.assert_called_once_with("test.csv", sep=";")


@patch("src.reading_files.pd.read_excel")
def test_read_transactions_from_excel(mock_read_excel: Mock) -> None:
    """Проверяет чтение операций из Excel-файла."""
    mock_read_excel.return_value = pd.DataFrame(
        [{"id": 1, "amount": 100}, {"id": 2, "amount": 200}]
    )

    result = read_transactions_from_excel("test.xlsx")

    assert len(result) == 2
    assert result[1]["amount"] == 200
    mock_read_excel.assert_called_once_with("test.xlsx")
