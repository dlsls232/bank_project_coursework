from unittest.mock import patch

from src.main import (
    filter_operations_by_description,
    filter_ruble_operations,
    get_operations_by_status,
    load_transactions,
    main,
    sort_operations_by_date,
)


def test_load_transactions_invalid_type() -> None:
    """Проверяет неверный тип файла."""
    assert load_transactions("4") == []


def test_load_transactions_json() -> None:
    """Проверяет загрузку JSON."""
    with patch("src.main.read_json_file", return_value=[{"id": 1}]) as mock:
        result = load_transactions("1")

    assert result == [{"id": 1}]
    mock.assert_called_once()


def test_load_transactions_csv() -> None:
    """Проверяет загрузку CSV."""
    with patch(
        "src.main.read_transactions_from_csv",
        return_value=[{"id": 1}],
    ) as mock:
        result = load_transactions("2")

    assert result == [{"id": 1}]
    mock.assert_called_once()


def test_load_transactions_excel() -> None:
    """Проверяет загрузку Excel."""
    with patch(
        "src.main.read_transactions_from_excel",
        return_value=[{"id": 1}],
    ) as mock:
        result = load_transactions("3")

    assert result == [{"id": 1}]
    mock.assert_called_once()


def test_get_operations_by_status() -> None:
    """Проверяет фильтрацию по статусу."""
    operations = [
        {"state": "EXECUTED"},
        {"state": "CANCELED"},
        {"state": "EXECUTED"},
    ]

    with patch("builtins.input", return_value="EXECUTED"):
        result = get_operations_by_status(operations)

    assert result == [
        {"state": "EXECUTED"},
        {"state": "EXECUTED"},
    ]


def test_get_operations_by_status_invalid_then_valid() -> None:
    """Проверяет повторный ввод после неверного статуса."""
    operations = [{"state": "CANCELED"}]

    with (
        patch("builtins.input", side_effect=["UNKNOWN", "CANCELED"]),
        patch("builtins.print") as mock_print,
    ):
        result = get_operations_by_status(operations)

    assert result == [{"state": "CANCELED"}]
    assert mock_print.call_count == 2


def test_get_operations_by_status_no_matches() -> None:
    """Проверяет отсутствие операций с нужным статусом."""
    operations = [{"state": "CANCELED"}]

    with patch("builtins.input", return_value="EXECUTED"):
        result = get_operations_by_status(operations)

    assert result == []


def test_get_operations_by_status_case_insensitive() -> None:
    """Проверяет нечувствительность статуса к регистру."""
    operations = [{"state": "executed"}]

    with patch("builtins.input", return_value="executed"):
        result = get_operations_by_status(operations)

    assert result == [{"state": "executed"}]


def test_sort_operations_by_date_ascending() -> None:
    """Проверяет сортировку по возрастанию."""
    operations = [
        {"date": "2025-02-01"},
        {"date": "2025-01-01"},
    ]

    with patch("builtins.input", side_effect=["да", "1"]):
        result = sort_operations_by_date(operations)

    assert result == [
        {"date": "2025-01-01"},
        {"date": "2025-02-01"},
    ]


def test_sort_operations_by_date_descending() -> None:
    """Проверяет сортировку по убыванию."""
    operations = [
        {"date": "2025-01-01"},
        {"date": "2025-02-01"},
    ]

    with patch("builtins.input", side_effect=["да", "2"]):
        result = sort_operations_by_date(operations)

    assert result == [
        {"date": "2025-02-01"},
        {"date": "2025-01-01"},
    ]


def test_sort_operations_by_date_no_sort() -> None:
    """Проверяет отказ от сортировки."""
    operations = [{"date": "2025-02-01"}, {"date": "2025-01-01"}]

    with patch("builtins.input", return_value="нет"):
        result = sort_operations_by_date(operations)

    assert result is operations


def test_sort_operations_by_date_missing_date() -> None:
    """Проверяет сортировку операций без даты."""
    operations = [
        {"date": "2025-01-01"},
        {"description": "Без даты"},
    ]

    with patch("builtins.input", side_effect=["да", "1"]):
        result = sort_operations_by_date(operations)

    assert result[0] == {"description": "Без даты"}
    assert result[1] == {"date": "2025-01-01"}


def test_filter_ruble_operations_yes() -> None:
    """Проверяет фильтрацию операций в рублях."""
    operations = [
        {"currency_code": "RUB"},
        {"currency_code": "USD"},
    ]

    with patch("builtins.input", return_value="да"):
        result = filter_ruble_operations(operations)

    assert result == [{"currency_code": "RUB"}]


def test_filter_ruble_operations_case_insensitive() -> None:
    """Проверяет фильтрацию с учётом регистра валюты."""
    operations = [{"currency_code": "rub"}, {"currency_code": "USD"}]

    with patch("builtins.input", return_value="да"):
        result = filter_ruble_operations(operations)

    assert result == [{"currency_code": "rub"}]


def test_filter_ruble_operations_missing_currency() -> None:
    """Проверяет операции без кода валюты."""
    operations = [{"description": "Без валюты"}]

    with patch("builtins.input", return_value="да"):
        result = filter_ruble_operations(operations)

    assert result == []


def test_filter_ruble_operations_no() -> None:
    """Проверяет отказ от фильтрации по валюте."""
    operations = [{"currency_code": "USD"}]

    with patch("builtins.input", return_value="нет"):
        result = filter_ruble_operations(operations)

    assert result is operations


def test_filter_operations_by_description_yes() -> None:
    """Проверяет поиск по описанию."""
    operations = [{"description": "Перевод клиенту"}]

    with (
        patch("builtins.input", side_effect=["да", "Перевод"]),
        patch("src.main.process_bank_search", return_value=operations) as mock,
    ):
        result = filter_operations_by_description(operations)

    assert result == operations
    mock.assert_called_once_with(operations, "Перевод")


def test_filter_operations_by_description_no() -> None:
    """Проверяет отказ от поиска по описанию."""
    operations = [{"description": "Перевод"}]

    with patch("builtins.input", return_value="нет"):
        result = filter_operations_by_description(operations)

    assert result is operations


def test_filter_operations_by_description_empty_word() -> None:
    """Проверяет пустое слово для поиска."""
    operations = [{"description": "Перевод"}]

    with patch("builtins.input", side_effect=["да", ""]):
        result = filter_operations_by_description(operations)

    assert result is operations


def test_main_invalid_file_type() -> None:
    """Проверяет неверный выбор источника данных."""
    with (
        patch("builtins.input", return_value="4"),
        patch("builtins.print") as mock_print,
        patch("src.main.load_transactions") as mock_load,
    ):
        main()

    mock_load.assert_not_called()
    mock_print.assert_any_call("Неверный выбор источника данных.")


def test_main_empty_transactions() -> None:
    """Проверяет обработку пустого списка операций."""
    with (
        patch("builtins.input", return_value="1"),
        patch("src.main.load_transactions", return_value=[]),
        patch("builtins.print") as mock_print,
    ):
        main()

    mock_print.assert_any_call("Не удалось загрузить операции или список пуст.")


def test_main_no_operations_after_filtering() -> None:
    """Проверяет отсутствие операций после фильтрации."""
    operations = [
        {"state": "CANCELED", "date": "2025-01-01"},
    ]

    with (
        patch(
            "builtins.input",
            side_effect=["1", "EXECUTED", "нет", "нет", "нет"],
        ),
        patch("src.main.load_transactions", return_value=operations),
        patch("builtins.print") as mock_print,
    ):
        main()

    mock_print.assert_any_call("Операции, подходящие под условия, не найдены.")


def test_main_prints_operations() -> None:
    """Проверяет вывод найденных операций."""
    operations = [
        {
            "state": "EXECUTED",
            "date": "2025-01-01",
            "currency_code": "RUB",
            "description": "Перевод",
        }
    ]

    with (
        patch(
            "builtins.input",
            side_effect=["1", "EXECUTED", "нет", "нет", "нет"],
        ),
        patch("src.main.load_transactions", return_value=operations),
        patch("builtins.print") as mock_print,
    ):
        main()

    mock_print.assert_any_call("\nСписок операций:")
    mock_print.assert_any_call(operations[0])
