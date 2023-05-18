from datetime import date

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    first_name: str
    id: str
    last_name: str
    profile_pic: str


class User(UserBase):
    created_at: date
    description: str | None
    is_tutor: bool
    updated_at: date

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    # Hidden fields for public read
    created_at: date
    description: str | None
    first_name: str
    id: str
    is_tutor: bool
    last_name: str
    profile_pic: str | None
    updated_at: date

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    description: str | None
    is_tutor: bool | None
