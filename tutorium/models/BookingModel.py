from datetime import date, datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    course_id: int
    start_time: datetime


class Booking(BookingBase):
    created_at: date
    end_time: datetime
    id: int
    student_id: str
    student_meeting_code: str
    tutor_meeting_code: str

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    pass


class BookingRead(Booking):
    course_description: str
    course_duration: int
    course_name: str
    course_picture_path: str | None
    tutor_first_name: str
    tutor_id: str
    tutor_last_name: str
