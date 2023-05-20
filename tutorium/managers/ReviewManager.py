from datetime import date, datetime

from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import BookingManager
from ..models import BookingModel, ReviewModel
from ..utils import Updater
from ..utils.Exceptions import BadRequestException, NotFoundException


def create(db: Session, review_create: ReviewModel.ReviewCreate, student_id: str):
    booking = BookingManager.get(db, booking_id=review_create.booking_id)
    _checks_on_booking(db, booking=booking, user_id=student_id)
    _create_update_checks(review=review_create)

    review_db = Schema.Review(
        **review_create.dict(),
        created_at=date.today(),
        student_id=student_id,
        updated_at=date.today(),
    )
    db.add(review_db)
    db.flush()
    return ReviewModel.Review.from_orm(review_db)


def delete(db: Session, review_id: int):
    review_db = get(db, review_id=review_id, as_db=True)
    db.delete(review_db)
    db.flush()


def get(db: Session, review_id: int, as_db: bool = False):
    review_db = db.query(Schema.Review).filter(Schema.Review.id == review_id).first()
    if review_db is None:
        raise NotFoundException(entity="review", id=review_id)

    return review_db if as_db else ReviewModel.Review.from_orm(review_db)


def get_all_by_course(db: Session, course_id: int):
    reviews = (
        db.query(Schema.Review)
        .filter(
            Schema.Review.booking_id.in_(
                [
                    booking.id
                    for booking in db.query(Schema.Booking)
                    .filter(Schema.Booking.course_id == course_id)
                    .all()
                ]
            )
        )
        .all()
    )
    return list(map(ReviewModel.Review.from_orm, reviews))


def update(db: Session, review_update: ReviewModel.ReviewUpdate):
    _create_update_checks(review=review_update)

    review_db = get(db, review_id=review_update.id, as_db=True)
    Updater.update(review_db, review_update)
    db.flush()
    return ReviewModel.Review.from_orm(review_db)


def does_student_own_the_review(db: Session, review_id: int, student_id: str):
    review_db = get(db, review_id=review_id)
    return review_db.student_id == student_id


def _is_booking_reviewed(db: Session, booking_id: int):
    review = (
        db.query(Schema.Review).filter(Schema.Review.booking_id == booking_id).first()
    )
    return review is not None


def _checks_on_booking(db: Session, booking: BookingModel.Booking, user_id: str):
    if booking.end_time > datetime.now():
        raise BadRequestException(
            entity="booking",
            id=booking.id,
            operation="POST",
            custom_message=f"Student with id {user_id} cannot review this booking yet because it is not passed. End Time: {booking.end_time}",
        )
    if _is_booking_reviewed(db, booking_id=booking.id):
        raise BadRequestException(
            entity="booking",
            id=booking.id,
            operation="POST",
            custom_message=f"Student with id {user_id} is already reviewed this booking with id {booking.id}",
        )


def _create_update_checks(review: ReviewModel.ReviewCreate | ReviewModel.ReviewUpdate):
    if review.comment and len(review.comment) < 10:
        raise BadRequestException(
            entity="review",
            id="",
            operation="POST|UPDATE",
            custom_message=f"Review comment cannot be smaller than ten characters. Given name: {review.comment}",
        )
    if review.rating and not (0 <= review.rating <= 10):
        raise BadRequestException(
            entity="review",
            id="",
            operation="POST|UPDATE",
            custom_message=f"Review rating should be in the interval [0, 10]. Given rating: {review.rating}",
        )
