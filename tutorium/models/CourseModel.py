from datetime import date

from pydantic import BaseModel


class CourseBase(BaseModel):
    description: str
    duration: int
    id: int
    name: str


class Course(CourseBase):
    created_at: date
    updated_at: date
    tutor_id: str

    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    pass


class CourseRead(Course):
    pass
