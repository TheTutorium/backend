from datetime import date

from pydantic import BaseModel


class WhiteboardBase(BaseModel):
    booking_id: int
    content: str
    created_at: date
    id: int
    updated_at: date


class Review(WhiteboardBase):
    class Config:
        orm_mode = True


class ReviewCreate(WhiteboardBase):
    pass


class ReviewRead(WhiteboardBase):
    class Config:
        orm_mode = True
