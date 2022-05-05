from datetime import datetime
from typing import Any

from app.models import User


def create_user_entity(**kwargs: Any) -> User:
    default_kwargs = {
        "id": 1,
        "username": "sawaca96",
        "email": "sawaca96@example.com",
        "password": "password",
        "created_at": datetime.now(),
        "updated_at": datetime.now(),
        "followings": [],
    }
    user = User(**dict(default_kwargs, **kwargs))
    return user
