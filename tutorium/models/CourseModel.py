from datetime import date

from pydantic import BaseModel


class CourseBase(BaseModel):
    created_at: date
    duration: int
    id: int
    name: str
    tutor_id: str
    updated_at: date


class Course(CourseBase):
    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    pass


class CourseRead(CourseBase):
    class Config:
        orm_mode = True
