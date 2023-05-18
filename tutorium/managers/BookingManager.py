from sqlalchemy.orm import Session
from datetime import date

from ..database import Schema
from ..models import BookingModel
from ..managers import UserManager


def create_booking(db: Session, booking: BookingModel.BookingCreate, user_id: str):
    assert not UserManager.is_tutor(db, user_id=user_id)

    db_booking = Schema.Booking(
        course_id=booking.course_id,
        created_at=date.today(),
        end_time=booking.end_time,
        start_time=booking.start_time,
        student_id=user_id,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_bookings_of_user(db: Session, user_id: str):
    return (
        db.query(Schema.Booking)  # Tutor
        .filter(
            Schema.Booking.course_id.in_(
                db.query(Schema.Course).filter(Schema.Course.tutor_id == user_id).all()
            )
        )
        .all()
        if UserManager.is_tutor(db, user_id=user_id)
        else db.query(Schema.Booking)
        .filter(Schema.Booking.student_id == user_id)
        .all()  # Student
    )
