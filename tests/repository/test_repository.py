from sqlalchemy.ext.asyncio import AsyncSession

from app import model
from app.repository import UserRepository


async def test_insert_user(session: AsyncSession) -> None:
    # given
    repo = UserRepository(session)
    user = model.User(username="test", email="test@example.com", password="test")
    await repo.add(user)

    row = await session.execute("SELECT * FROM users")
    assert row == user


async def test_get_user_by_id() -> None:
    ...
