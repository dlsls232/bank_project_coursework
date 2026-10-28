from src.services import simple_search


def test_search_by_description() -> None:
    transactions = [
        {"Описание": "Покупка в Магните", "Категория": "Супермаркеты"},
        {"Описание": "Оплата интернета", "Категория": "Связь"},
    ]

    result = simple_search(transactions, "Магните")

    assert result == [transactions[0]]


def test_search_by_category() -> None:
    transactions = [
        {"Описание": "Покупка продуктов", "Категория": "Супермаркеты"},
        {"Описание": "Оплата интернета", "Категория": "Связь"},
    ]

    result = simple_search(transactions, "супермаркеты")

    assert result == [transactions[0]]


def test_search_is_case_insensitive() -> None:
    transactions = [
        {"Описание": "Покупка в МАГНИТЕ", "Категория": "Супермаркеты"},
    ]

    result = simple_search(transactions, "магните")

    assert result == [transactions[0]]


def test_search_strips_spaces() -> None:
    transactions = [
        {"Описание": "Покупка в Магните", "Категория": "Супермаркеты"},
    ]

    result = simple_search(transactions, "  Магните  ")

    assert result == [transactions[0]]


def test_search_empty_query() -> None:
    transactions = [
        {"Описание": "Покупка в Магните", "Категория": "Супермаркеты"},
    ]

    assert simple_search(transactions, "") == []
    assert simple_search(transactions, "   ") == []


def test_search_no_matches() -> None:
    transactions = [
        {"Описание": "Покупка в Магните", "Категория": "Супермаркеты"},
    ]

    assert simple_search(transactions, "Такси") == []


def test_search_missing_fields() -> None:
    transactions = [
        {},
        {"Описание": "Оплата интернета"},
        {"Категория": "Супермаркеты"},
    ]

    result = simple_search(transactions, "супермаркеты")

    assert result == [transactions[2]]
