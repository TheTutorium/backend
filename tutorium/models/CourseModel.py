from datetime import date

from pydantic import BaseModel


class CourseBase(BaseModel):
    description: str
    duration: int
    name: str


class Course(CourseBase):
    created_at: date
    picture_path: str | None = None
    deactivated: bool
    id: int
    updated_at: date
    tutor_id: str

    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    pass


class CourseRead(Course):
    tutor_first_name: str
    tutor_last_name: str


class CourseUpdate(BaseModel):
    description: str | None = None
    duration: int | None = None
    id: int
    name: str | None = None
