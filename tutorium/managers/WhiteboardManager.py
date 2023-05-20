from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import WhiteboardModel
from ..utils.Exceptions import BadRequestException, NotFoundException


def create(db: Session, whiteboard_create: WhiteboardModel.WhiteboardCreate):
    _create_checks(db, booking_id=whiteboard_create.booking_id)

    whiteboard_db = Schema.Whiteboard(
        **whiteboard_create.dict(),
        created_at=date.today(),
    )
    db.add(whiteboard_db)
    db.flush()
    return WhiteboardModel.Whiteboard.from_orm(whiteboard_db)


def get_by_booking_id(db: Session, booking_id: int):
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


def _does_booking_have_whiteboard(db: Session, booking_id: int):
    whiteboard = (
        db.query(Schema.Whiteboard)
        .filter(Schema.Whiteboard.booking_id == booking_id)
        .first()
    )
    return whiteboard is not None


def _create_checks(db: Session, booking_id: int):
    if _does_booking_have_whiteboard(db, booking_id=booking_id):
        raise BadRequestException(
            entity="whiteboard",
            id="",
            operation="POST",
            custom_message=f"Booking with id {booking_id} is already have a whiteboard.",
        )
