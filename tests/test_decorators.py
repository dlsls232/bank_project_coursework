from pathlib import Path

import pytest

from src.decorators import log


def test_log_success_console(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def add(x: int, y: int) -> int:
        return x + y

    result = add(1, 2)
    captured = capsys.readouterr()

    assert result == 3
    assert "add ok" in captured.out


def test_log_error_console(capsys: pytest.CaptureFixture[str]) -> None:
    @log()
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    captured = capsys.readouterr()

    assert "divide error:" in captured.out
    assert "Inputs: (1, 0), {}" in captured.out


def test_log_success_file(tmp_path: Path) -> None:
    filename = tmp_path / "mylog.txt"

    @log(filename=str(filename))
    def add(x: int, y: int) -> int:
        return x + y

    result = add(2, 3)

    assert result == 5
    assert "add ok" in filename.read_text(encoding="utf-8")


def test_log_error_file(tmp_path: Path) -> None:
    filename = tmp_path / "mylog.txt"

    @log(filename=str(filename))
    def divide(x: int, y: int) -> float:
        return x / y

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    content = filename.read_text(encoding="utf-8")

    assert "divide error:" in content
    assert "Inputs: (1, 0), {}" in content
