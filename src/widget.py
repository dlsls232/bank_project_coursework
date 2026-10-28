from datetime import datetime

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(value: str) -> str:
    """Маскирует номер карты или счета."""
    name, number = value.rsplit(" ", 1)

    if name == "Счет":
        masked_number = get_mask_account(number)
    else:
        masked_number = get_mask_card_number(number)

    return f"{name} {masked_number}"


def get_date(date_string: str) -> str:
    """Преобразует дату в формат ДД.ММ.ГГГГ."""
    date = datetime.fromisoformat(date_string)
    return date.strftime("%d.%m.%Y")
