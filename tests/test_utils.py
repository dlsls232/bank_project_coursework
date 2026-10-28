import json
from pathlib import Path
from unittest.mock import mock_open, patch

from src.utils import read_json_file


def test_read_json_file_success() -> None:
    """Проверяет успешное чтение JSON."""
    data = [{"id": 1, "amount": 100}]

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = read_json_file("test.json")

    assert result == data


def test_read_json_file_not_found() -> None:
    """Проверяет обработку отсутствующего файла."""
    with patch("builtins.open", side_effect=FileNotFoundError):
        result = read_json_file("missing.json")

    assert result == []


def test_read_json_file_invalid_json() -> None:
    """Проверяет обработку неправильного JSON."""
    with patch("builtins.open", mock_open(read_data="{invalid json")):
        result = read_json_file("invalid.json")

    assert result == []


def test_read_json_file_wrong_format() -> None:
    """Проверяет обработку неподходящего формата данных."""
    data = {"id": 1, "amount": 100}

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = read_json_file("wrong_format.json")

    assert result == []


def test_read_json_file_accepts_path() -> None:
    """Проверяет передачу пути в виде объекта Path."""
    data = [{"id": 2}]

    with patch("builtins.open", mock_open(read_data=json.dumps(data))):
        result = read_json_file(Path("test.json"))

    assert result == data
