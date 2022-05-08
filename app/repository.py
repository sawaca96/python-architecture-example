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

    async def update(
        self,
        user_id: int,
        *,
        username: str,
        email: EmailStr,
        bio: str,
        image: str,
    ) -> models.User:
        ...

    async def follow(self, user: models.User) -> bool:
        ...

    async def unfollow(self, user: models.User) -> bool:
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
            'SELECT * FROM "user" u LEFT OUTER JOIN follower_x_following f'
            " ON f.follower_id = u.id WHERE id = :user_id",
            {"user_id": user_id},
        )
        rows = [dict(r) for r in result.all()]
        followings = [r["following_id"] for r in rows]
        return models.User(**rows[0], followings=followings)

    async def update(
        self,
        user_id: int,
        *,
        username: str,
        email: EmailStr,
        bio: str,
        image: str,
    ) -> models.User:
        result: CursorResult = await self.session.execute(
            'UPDATE "user" SET username = :username, email = :email,'
            " bio = :bio, image = :image"
            " WHERE id = :user_id RETURNING id, username, email, bio, image",
            dict(user_id=user_id, username=username, email=email, bio=bio, image=image),
        )
        row = dict(result.fetchone())
        return models.User(**row)

    async def follow(self, user: models.User) -> bool:
        try:
            await self.session.execute(
                "INSERT INTO follower_x_following (follower_id, following_id)"
                " VALUES (:follower_id, :following_id)"
                " ON CONFLICT ON CONSTRAINT pk_follower_x_following DO NOTHING"
                " RETURNING follower_id, following_id",
                [
                    dict(follower_id=user.id, following_id=following_id)
                    for following_id in user.followings
                ],
            )
            return True
        except Exception:
            return False

    async def unfollow(self, user: models.User) -> bool:
        try:
            if len(user.followings) == 1:
                # TODO: tuple이 한개일 경우 마지막에 콤마가 붙는데 bind시 삭제하는 법 못찾음.
                await self.session.execute(
                    "DELETE FROM follower_x_following"
                    " WHERE follower_id = :follower_id AND"
                    " following_id != :following_id",
                    dict(follower_id=user.id, following_id=user.followings[0]),
                )
            else:
                await self.session.execute(
                    "DELETE FROM follower_x_following"
                    " WHERE follower_id = :follower_id AND"
                    " following_id NOT IN :following_ids",
                    dict(follower_id=user.id, following_ids=tuple(user.followings)),
                )
            return True
        except Exception:
            return False
