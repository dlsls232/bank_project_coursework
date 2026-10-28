import json
import logging
from pathlib import Path
from typing import Any

LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    LOG_DIR / "utils.log",
    mode="w",
    encoding="utf-8",
)
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def read_json_file(file_path: str | Path) -> list[dict[str, Any]]:
    """Читает JSON-файл и возвращает список словарей с данными."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError) as error:
        logger.error("Не удалось прочитать JSON-файл %s: %s", file_path, error)
        return []

    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        logger.debug("JSON-файл успешно прочитан: %s", file_path)
        return data

    logger.error("JSON-файл содержит данные неподходящего формата: %s", file_path)
    return []
