from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import WhiteboardModel
from ..utils.Exceptions import NotFoundException


def create(db: Session, whiteboard_create: WhiteboardModel.WhiteboardCreate):
    _create_checks(db, booking_id=whiteboard_create.booking_id)

    whiteboard_db = Schema.Whiteboard(
        **whiteboard_create.dict(),
        created_at=date.today(),
    )
    db.add(whiteboard_db)
    db.flush()
    return WhiteboardModel.Whiteboard.from_orm(whiteboard_db)


def delete(db: Session, booking_id: int):
    whiteboard_db = get_by_booking_id(db, booking_id=booking_id, as_db=True)
    db.delete(whiteboard_db)
    db.flush()


def get_by_booking_id(db: Session, booking_id: int, as_db: bool = False):
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

    return (
        whiteboard_db if as_db else WhiteboardModel.Whiteboard.from_orm(whiteboard_db)
    )


def _create_checks(db: Session, booking_id: int):
    try:
        delete(db, booking_id=booking_id)
    except NotFoundException:
        pass
