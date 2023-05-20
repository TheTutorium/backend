from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    description: str
    first_name: str
    id: str
    is_tutor: bool
    last_name: str
    profile_pic: str | None = None


class User(UserBase):
    created_at: date
    email: str
    updated_at: date

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: str


class UserRead(User):
    pass


class PublicUserRead(UserBase):
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    description: str | None = None
    profile_pic: str | None = None
