from sqlalchemy.orm import Session
from datetime import date

from ..database import Schema
from ..models import WhiteboardModel


def create_whiteboard(db: Session, whiteboard: WhiteboardModel.WhiteboardCreate):
    db_whiteboard = Schema.Course(
        created_at=date.today(),
        booking_id=whiteboard.booking_id,
        content=whiteboard.content,
    )
    db.add(db_whiteboard)
    db.commit()
    db.refresh(db_whiteboard)
    return db_whiteboard


def get_whiteboard(db: Session, whiteboard_id: int):
    return db.query(Schema.Whiteboard).filter(Schema.Whiteboard.id == whiteboard_id).first()  # type: ignore


def get_whiteboards(db: Session):
    return db.query(Schema.Whiteboard).all()
