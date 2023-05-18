from datetime import date, datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    course_id: int
    end_time: datetime
    start_time: datetime


class Booking(BookingBase):
    created_at: date
    id: int
    student_id: str
    student_meeting_code: str
    tutor_meeting_code: str

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    pass


class BookingRead(Booking):
    pass
