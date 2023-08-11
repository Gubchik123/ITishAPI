from functools import wraps
from typing import Callable

from sqlalchemy.orm.exc import NoResultFound
from fastapi.exceptions import HTTPException


def catch_model_not_fount(model: str) -> Callable:
    """Returns decorator for catching model not found exception."""

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs):
            """Wraps function for catching model not found exception."""
            try:
                return func(*args, **kwargs)
            except NoResultFound:
                raise HTTPException(
                    status_code=404, detail=f"{model} not found"
                )

        return inner

    return wrapper
