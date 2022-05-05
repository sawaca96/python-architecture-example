from __future__ import annotations

from datetime import datetime

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
    password: str
    created_at: datetime
    updated_at: datetime
    followings: list[User]

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id
        return False

    def follow(self, user: User) -> None:
        if user not in self.followings:
            self.followings.append(user)
        else:
            raise FollowError

    def unfollow(self, user: User) -> None:
        if user in self.followings:
            self.followings.remove(user)
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
