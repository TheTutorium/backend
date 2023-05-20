from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import ReviewModel
from ..utils import Updater
from ..utils.Exceptions import NotFoundException


def create(db: Session, review_create: ReviewModel.ReviewCreate, student_id: str):
    review_db = Schema.Review(
        **review_create.dict(),
        created_at=date.today(),
        student_id=student_id,
        updated_at=date.today(),
    )
    db.add(review_db)
    db.commit()
    db.refresh(review_db)
    return ReviewModel.Review.from_orm(review_db)


def delete(db: Session, review_id: int):
    review_db = get(db, review_id=review_id, as_db=True)
    db.delete(review_db)
    db.commit()


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
    review_db = get(db, review_id=review_update.id, as_db=True)
    Updater.update(review_db, review_update)
    db.commit()
    db.refresh(review_db)
    return ReviewModel.Review.from_orm(review_db)


def does_student_own_review(db: Session, review_id: int, student_id):
    review_db = get(db, review_id=review_id)
    return review_db.student_id == student_id
