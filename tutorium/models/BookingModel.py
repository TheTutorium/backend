from datetime import date, datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    course_id: int
    end_time: datetime
    id: int
    start_time: datetime


class Booking(BookingBase):
    created_at: date

    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    pass


class BookingRead(Booking):
    pass
