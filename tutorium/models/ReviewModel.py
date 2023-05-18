from datetime import date

from pydantic import BaseModel


class ReviewBase(BaseModel):
    booking_id: int
    comment: str
    id: int
    rating: int


class Review(ReviewBase):
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(Review):
    pass
