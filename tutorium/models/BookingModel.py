from datetime import date, datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    course_id: int
    created_at: date
    end_time: datetime
    id: int
    start_time: datetime


class Booking(BookingBase):
    class Config:
        orm_mode = True


class BookingCreate(BookingBase):
    pass


class BookingRead(BookingBase):
    class Config:
        orm_mode = True
