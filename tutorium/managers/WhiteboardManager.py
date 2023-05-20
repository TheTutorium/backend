from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import WhiteboardModel
from ..utils.Exceptions import NotFoundException, UnauthorizedException
from . import BookingManager


def create(
    db: Session, tutor_id: str, whiteboard_create: WhiteboardModel.WhiteboardCreate
):
    if not BookingManager.is_user_in_booking(
        db, booking_id=whiteboard_create.booking_id, user_id=tutor_id
    ):
        raise UnauthorizedException(
            user_id=tutor_id,
            custom_message=f"Tutow with id {tutor_id} is not in this booking with id {whiteboard_create.booking_id}",
        )

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
        raise UnauthorizedException(
            user_id=user_id,
            custom_message=f"User with id {user_id} is not in this booking with id {booking_id}",
        )

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
