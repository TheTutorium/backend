from sqlalchemy.orm import Session
from datetime import date

from ..database import Schema
from ..models import BookingModel


def create_booking(db: Session, booking: BookingModel.BookingCreate):
    db_booking = Schema.Course(
        course_id=booking.course_id,
        created_at=date.today(),
        end_time=booking.end_time,
        start_time=booking.start_time,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int):
    return db.query(Schema.Booking).filter(Schema.Booking.id == booking_id).first()  # type: ignore


def get_bookings(db: Session):
    return db.query(Schema.Booking).all()
