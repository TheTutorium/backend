from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import ReviewModel
from . import UserManager


def create(db: Session, create_review: ReviewModel.ReviewCreate, student_id: str):
    assert not UserManager.is_tutor(db, user_id=student_id)

    review = Schema.Review(
        **create_review.dict(),
        created_at=date.today(),
        student_id=student_id,
        updated_at=date.today(),
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review


def get_all_of_course(db: Session, course_id: int):
    return (
        db.query(Schema.Review)
        .filter(
            Schema.Review.booking_id.in_(
                db.query(Schema.Booking)
                .filter(Schema.Booking.course_id == course_id)
                .all()
            )
        )
        .first()
    )
