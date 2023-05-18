from datetime import date

from pydantic import BaseModel


class CourseBase(BaseModel):
    course_pic: str | None
    description: str
    duration: int
    name: str


class Course(CourseBase):
    created_at: date
    id: int
    updated_at: date
    tutor_id: str

    class Config:
        orm_mode = True


class CourseCreate(CourseBase):
    pass


class CourseRead(Course):
    pass
