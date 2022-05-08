from __future__ import annotations

from pydantic import BaseModel, EmailStr


class FollowError(Exception):
    pass


class UnfollowError(Exception):
    pass


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    image: str | None = None
    followings: list[int] = []

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id
        return False

    def follow(self, user_id: int) -> None:
        if user_id not in self.followings:
            self.followings.append(user_id)
        else:
            raise FollowError

    def unfollow(self, user_id: int) -> None:
        if user_id in self.followings:
            self.followings.remove(user_id)
        else:
            raise UnfollowError


class Article(BaseModel):
    slug: str
    title: str
    description: str
    body: str
    tags: list[str]
    author: User
    favorited: bool
    favorites_count: int


class Comment(BaseModel):
    body: str
    author: User
