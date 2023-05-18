from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import UserManager
from ..models import BookingModel


def create(db: Session, booking_create: BookingModel.BookingCreate, student_id: str):
    assert not UserManager.is_tutor(db, user_id=student_id)

    booking = Schema.Booking(
        **booking_create.dict(),
        created_at=date.today(),
        student_id=student_id,
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_all_of_user(db: Session, user_id: str):
    if UserManager.is_tutor(db, user_id=user_id):
        return (
            db.query(Schema.Booking)
            .filter(
                Schema.Booking.course_id.in_(
                    db.query(Schema.Course)
                    .filter(Schema.Course.tutor_id == user_id)
                    .all()
                )
            )
            .all()
        )
    else:
        return (
            db.query(Schema.Booking).filter(Schema.Booking.student_id == user_id).all()
        )
