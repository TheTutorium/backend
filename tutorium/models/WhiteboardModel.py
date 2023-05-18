from datetime import date

from pydantic import BaseModel


class WhiteboardBase(BaseModel):
    booking_id: int
    content: str
    id: int


class Whiteboard(WhiteboardBase):
    created_at: date
    updated_at: date

    class Config:
        orm_mode = True


class WhiteboardCreate(WhiteboardBase):
    pass


class ReviewRead(Whiteboard):
    pass
