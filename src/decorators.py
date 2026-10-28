import logging
from functools import wraps
from typing import Callable, ParamSpec, TypeVar

P = ParamSpec("P")
R = TypeVar("R")


def log(
    filename: str | None = None,
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Логирует результат выполнения функции или ошибку."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        """Оборачивает функцию и записывает результат её выполнения или ошибку."""

        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            if filename is not None:
                logging.basicConfig(
                    filename=filename,
                    level=logging.INFO,
                    format="%(message)s",
                    force=True,
                )

            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"
                if filename is None:
                    print(message)
                else:
                    logging.info(message)
                return result
            except Exception as error:
                message = (
                    f"{func.__name__} error: {error}. " f"Inputs: {args}, {kwargs}"
                )
                if filename is None:
                    print(message)
                else:
                    logging.error(message)
                raise

        return wrapper

    return decorator
