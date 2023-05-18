from datetime import date

from pydantic import BaseModel


class ReviewBase(BaseModel):
    booking_id: int
    comment: str
    rating: int


class Review(ReviewBase):
    created_at: date
    id: int
    student_id: str
    updated_at: date

    class Config:
        orm_mode = True


class ReviewCreate(ReviewBase):
    pass


class ReviewRead(Review):
    pass


class ReviewUpdate(BaseModel):
    comment: str | None = None
    id: int
    rating: int | None = None
