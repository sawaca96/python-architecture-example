from typing import Any

from app.models import User


def create_user_entity(**kwargs: Any) -> User:
    default_kwargs = {
        "id": 1,
        "username": "jake",
        "email": "jake@jake.jake",
    }
    user = User(**dict(default_kwargs, **kwargs))
    return user
