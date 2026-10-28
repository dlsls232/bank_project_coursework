from src.search import process_bank_operations, process_bank_search


def test_process_bank_search() -> None:
    """Проверяет поиск операций по описанию без учёта регистра."""
    data = [
        {"description": "Card transfer"},
        {"description": "Supermarket payment"},
        {"description": "Money transfer"},
    ]

    result = process_bank_search(data, "TRANSFER")

    assert len(result) == 2
    assert result[0]["description"] == "Card transfer"
    assert result[1]["description"] == "Money transfer"


def test_process_bank_search_no_matches() -> None:
    """Проверяет поиск, если совпадений нет."""
    data = [{"description": "Card transfer"}]

    assert process_bank_search(data, "payment") == []


def test_process_bank_operations() -> None:
    """Проверяет подсчёт операций по категориям."""
    data = [
        {"description": "Transfer"},
        {"description": "Payment"},
        {"description": "Transfer"},
    ]

    result = process_bank_operations(data, ["Transfer", "Payment", "Withdrawal"])

    assert result == {
        "Transfer": 2,
        "Payment": 1,
        "Withdrawal": 0,
    }
