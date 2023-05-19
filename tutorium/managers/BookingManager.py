from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import UserManager
from ..models import BookingModel
from ..utils import StringUtils


def create(db: Session, booking_create: BookingModel.BookingCreate, student_id: str):
    if UserManager.is_tutor(db, user_id=student_id):
        raise Exception

    booking = Schema.Booking(
        **booking_create.dict(),
        created_at=date.today(),
        student_id=student_id,
        student_meeting_code=StringUtils.random_string(15),
        tutor_meeting_code=StringUtils.random_string(15),
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def delete(db: Session, booking_id: int, user_id: str):
    if not is_user_in_booking(db, booking_id=booking_id, user_id=user_id):
        raise Exception

    booking = get(db, booking_id=booking_id)
    db.delete(booking)
    db.commit()


def get(db: Session, booking_id: int):
    booking = db.query(Schema.Booking).filter(Schema.Booking.id == booking_id).first()
    if booking is None:
        raise Exception

    return booking


def get_all_by_user(db: Session, user_id: str):
    if UserManager.is_tutor(db, user_id=user_id):
        return (
            db.query(Schema.Booking)
            .filter(
                Schema.Booking.course_id.in_(
                    [
                        course.id
                        for course in db.query(Schema.Course)
                        .filter(Schema.Course.tutor_id == user_id)
                        .all()
                    ]
                )
            )
            .all()
        )
    else:
        return (
            db.query(Schema.Booking).filter(Schema.Booking.student_id == user_id).all()
        )


def is_user_in_booking(db: Session, booking_id: int, user_id: str):
    bookings = get_all_by_user(db, user_id=user_id)
    return booking_id in [b.id for b in bookings]
