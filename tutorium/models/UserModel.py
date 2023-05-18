from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    created_at: date
    email: str
    first_name: str
    id: str
    last_name: str
    profile_pic: str
    updated_at: date


class User(UserBase):
    description: str | None
    is_tutor: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    description: str | None
    first_name: str
    id: str
    is_tutor: bool
    last_name: str
    profile_pic: str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    description: str | None
    is_tutor: bool | None
