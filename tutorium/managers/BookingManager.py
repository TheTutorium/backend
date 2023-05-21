from datetime import date, datetime

from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import CourseManager, UserManager
from ..models import BookingModel
from ..utils import StringUtils
from ..utils.Exceptions import BadRequestException, NotFoundException


def create(db: Session, booking_create: BookingModel.BookingCreate, student_id: str):
    # TODO
    booking_db = Schema.Booking(
        **booking_create.dict(),
        created_at=date.today(),
        duration=60,
        student_id=student_id,
        student_meeting_code=StringUtils.random_string(15),
        tutor_meeting_code=StringUtils.random_string(15),
    )
    db.add(booking_db)
    db.flush()
    return BookingModel.Booking.from_orm(booking_db)


def delete(db: Session, booking_id: int):
    booking_db = get(db, booking_id=booking_id, as_db=True)
    _delete_checks(booking_db=booking_db)

    db.delete(booking_db)
    db.flush()


def get(db: Session, booking_id: int, as_db: bool = False):
    booking_db = (
        db.query(Schema.Booking).filter(Schema.Booking.id == booking_id).first()
    )
    if booking_db is None:
        raise NotFoundException(entity="booking", id=booking_id)

    return booking_db if as_db else BookingModel.Booking.from_orm(booking_db)


def get_all_by_user(db: Session, user_id: str):
    if UserManager.is_tutor(db, user_id=user_id):
        bookings_db = (
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
        bookings_db = (
            db.query(Schema.Booking).filter(Schema.Booking.student_id == user_id).all()
        )

    return list(map(BookingModel.Booking.from_orm, bookings_db))


def is_user_in_booking(db: Session, booking_id: int, user_id: str):
    return is_student_in_booking(
        db, booking_id=booking_id, student_id=user_id
    ) or _is_tutor_in_booking(db, booking_id=booking_id, tutor_id=user_id)


def is_student_in_booking(db: Session, booking_id: int, student_id: str):
    booking = get(db, booking_id=booking_id)
    return booking.student_id == student_id


def _is_tutor_in_booking(db: Session, booking_id: int, tutor_id: str):
    booking = get(db, booking_id=booking_id)
    course = CourseManager.get(db, course_id=booking.course_id)
    return course.tutor_id == tutor_id


def _delete_checks(booking_db: Schema.Booking):
    if booking_db.start_time < datetime.now():
        raise BadRequestException(
            entity="booking",
            id=int(booking_db.id),
            operation="DELETE",
            custom_message=f"Booking with id {booking_db.id} cannot be deleted because its is already passed. Start time: {booking_db.start_time}",
        )
