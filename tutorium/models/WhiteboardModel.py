from datetime import date

from pydantic import BaseModel


class WhiteboardBase(BaseModel):
    booking_id: int
    content: str


class Whiteboard(WhiteboardBase):
    created_at: date
    id: int

    class Config:
        orm_mode = True


class WhiteboardCreate(WhiteboardBase):
    pass


class WhiteboardRead(Whiteboard):
    pass
