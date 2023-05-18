from datetime import date

from pydantic import BaseModel


class ReviewBase(BaseModel):
    booking_id: int
    comment: str
    created_at: date
    id: int
    rating: int
    updated_at: date


class Review(ReviewBase):
    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(ReviewBase):
    class Config:
        orm_mode = True
