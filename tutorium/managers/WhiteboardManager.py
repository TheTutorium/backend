from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import WhiteboardModel
from . import BookingManager


def create(
    db: Session, user_id: str, whiteboard_create: WhiteboardModel.WhiteboardCreate
):
    if not BookingManager.is_user_in_booking(
        db, booking_id=whiteboard_create.booking_id, user_id=user_id
    ):
        raise Exception

    whiteboard_db = Schema.Whiteboard(
        **whiteboard_create.dict(),
        created_at=date.today(),
    )
    db.add(whiteboard_db)
    db.commit()
    db.refresh(whiteboard_db)
    return WhiteboardModel.Whiteboard.from_orm(whiteboard_db)


def get_by_booking_id(db: Session, booking_id: int, user_id: str):
    if not BookingManager.is_user_in_booking(
        db, booking_id=booking_id, user_id=user_id
    ):
        raise Exception

    whiteboard_db = (
        db.query(Schema.Whiteboard)
        .filter(Schema.Whiteboard.booking_id == booking_id)
        .first()
    )
    if whiteboard_db is None:
        raise Exception

    return WhiteboardModel.Whiteboard.from_orm(whiteboard_db)
