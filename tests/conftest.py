from typing import Any

import pytest


@pytest.fixture
def operations() -> list[dict[str, Any]]:
    """Тестовые данные для операций с разными статусами и датами."""
    return [
        {"id": 1, "state": "EXECUTED", "date": "2025-01-15T10:00:00"},
        {"id": 2, "state": "CANCELED", "date": "2025-01-20T10:00:00"},
        {"id": 3, "state": "EXECUTED", "date": "2025-01-10T10:00:00"},
        {"id": 4, "state": "PENDING", "date": "2025-01-15T10:00:00"},
    ]
