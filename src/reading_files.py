from typing import Any, cast

import pandas as pd


def read_transactions_from_csv(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из CSV-файла."""
    transactions = pd.read_csv(file_path, sep=";")
    records = transactions.to_dict(orient="records")
    return cast(list[dict[str, Any]], records)


def read_transactions_from_excel(file_path: str) -> list[dict[str, Any]]:
    """Считывает финансовые операции из Excel-файла."""
    transactions = pd.read_excel(file_path)
    records = transactions.to_dict(orient="records")
    return cast(list[dict[str, Any]], records)
