from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import ReviewModel
from . import UserManager


def create(db: Session, review_create: ReviewModel.ReviewCreate, student_id: str):
    if UserManager.is_tutor(db, user_id=student_id):
        raise Exception

    review = Schema.Review(
        **review_create.dict(),
        created_at=date.today(),
        student_id=student_id,
        updated_at=date.today(),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def delete(db: Session, review_id: int, student_id: str):
    review = get(db, review_id=review_id)
    if review.student_id != student_id:
        raise Exception

    db.delete(review)
    db.commit()


def get(db: Session, review_id: int):
    review = db.query(Schema.Review).filter(Schema.Review.id == review_id).first()

    if review is None:
        raise Exception

    return review


def get_all_by_course(db: Session, course_id: int):
    return (
        db.query(Schema.Review)
        .filter(
            Schema.Review.booking_id.in_(
                db.query(Schema.Booking)
                .filter(Schema.Booking.course_id == course_id)
                .all()
            )
        )
        .all()
    )
