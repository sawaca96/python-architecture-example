from __future__ import annotations

from pydantic import BaseModel, EmailStr


class User(BaseModel):
    id: int
    username: str
    email: EmailStr
    bio: str | None = None
    image: str | None = None

    def __eq__(self, o: object) -> bool:
        if isinstance(o, User):
            return self.id == o.id
        return False


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
