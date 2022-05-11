import abc

from pydantic import EmailStr
from sqlalchemy.engine.cursor import CursorResult
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


class UserRepository(abc.ABC):
    async def create(
        self,
        *,
        username: str,
        email: EmailStr,
        password: str,
    ) -> models.User:
        ...

    async def get_by_id(self, user_id: int) -> models.User:
        ...

    async def update(self, user: models.User) -> None:
        ...

    async def follow(self, from_user: models.User, to_user: models.User) -> None:
        ...

    async def unfollow(self, from_user: models.User, to_user: models.User) -> None:
        ...


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
        self,
        *,
        username: str,
        email: EmailStr,
        password: str,
    ) -> models.User:
        result: CursorResult = await self.session.execute(
            'INSERT INTO "user" (username, email, password)'
            " VALUES (:username, :email, :password) RETURNING id, username, email",
            {"username": username, "email": email, "password": password},
        )
        row = dict(result.fetchone())
        return models.User(**row)

    async def get_by_id(self, user_id: int) -> models.User:
        result: CursorResult = await self.session.execute(
            'SELECT * FROM "user" u WHERE id = :user_id',
            {"user_id": user_id},
        )
        row = dict(result.fetchone())
        return models.User(**row)

    async def update(self, user: models.User) -> None:
        await self.session.execute(
            'UPDATE "user" SET username = :username, email = :email,'
            " bio = :bio, image = :image WHERE id = :id ",
            user.dict(),
        )

    async def follow(self, from_user: models.User, to_user: models.User) -> None:
        await self.session.execute(
            "INSERT INTO follower_x_following (follower_id, following_id)"
            " VALUES (:follower_id, :following_id)",
            dict(follower_id=from_user.id, following_id=to_user.id),
        )

    async def unfollow(self, from_user: models.User, to_user: models.User) -> None:
        await self.session.execute(
            "DELETE FROM follower_x_following"
            " WHERE follower_id = :follower_id AND"
            " following_id = :following_id",
            dict(follower_id=from_user.id, following_id=to_user.id),
        )
