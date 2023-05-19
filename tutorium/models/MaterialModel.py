from datetime import date

from pydantic import BaseModel


class MaterialBase(BaseModel):
    course_id: int
    name: str


class Material(MaterialBase):
    created_at: date
    id: int
    path: str

    class Config:
        orm_mode = True


class MaterialCreate(MaterialBase):
    pass


class MaterialRead(MaterialBase):
    created_at: date
    id: int

    class Config:
        orm_mode = True
