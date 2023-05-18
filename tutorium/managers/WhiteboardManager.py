from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import WhiteboardModel


def create_whiteboard(db: Session, whiteboard_create: WhiteboardModel.WhiteboardCreate):
    whiteboard = Schema.Course(
        **whiteboard_create.dict(),
        created_at=date.today(),
    )
    db.add(whiteboard)
    db.commit()
    db.refresh(whiteboard)
    return whiteboard


def get_by_booking_id(db: Session, booking_id: int):
    return (
        db.query(Schema.Whiteboard)
        .filter(Schema.Whiteboard.booking_id == booking_id)
        .first()
    )
