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
