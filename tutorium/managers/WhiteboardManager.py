from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import WhiteboardModel
from ..utils.Exceptions import NotFoundException


def create(db: Session, whiteboard_create: WhiteboardModel.WhiteboardCreate):
    whiteboard_db = Schema.Whiteboard(
        **whiteboard_create.dict(),
        created_at=date.today(),
    )
    db.add(whiteboard_db)
    db.flush()
    return WhiteboardModel.Whiteboard.from_orm(whiteboard_db)


def get_by_booking_id(db: Session, booking_id: int, user_id: str):
    whiteboard_db = (
        db.query(Schema.Whiteboard)
        .filter(Schema.Whiteboard.booking_id == booking_id)
        .first()
    )
    if whiteboard_db is None:
        raise NotFoundException(
            entity="whiteboard",
            id="",
            custom_message=f"Booking with id {booking_id} does not have a whiteboard save",
        )

    return WhiteboardModel.Whiteboard.from_orm(whiteboard_db)
