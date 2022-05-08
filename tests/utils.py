from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


def create_user_entity(**kwargs: Any) -> User:
    default_kwargs = {
        "id": 1,
        "username": "jake",
        "email": "jake@jake.jake",
    }
    user = User(**dict(default_kwargs, **kwargs))
    return user


async def insert_user(session: AsyncSession, **kwargs: Any) -> User:
    default_kwargs = {
        "username": "jake",
        "email": "jake@jake.jake",
        "password": "password",
    }
    result = await session.execute(
        'INSERT INTO "user" (username, email, password) VALUES'
        " (:username, :email, :password) RETURNING id, username, email",
        dict(default_kwargs, **kwargs),
    )
    row = result.fetchone()
    return User(**row)
