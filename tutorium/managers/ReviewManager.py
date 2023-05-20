from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import ReviewModel
from . import UserManager


def create(db: Session, review_create: ReviewModel.ReviewCreate, student_id: str):
    if UserManager.is_tutor(db, user_id=student_id):
        raise Exception

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


def delete(db: Session, review_id: int, student_id: str):
    review_db = get(db, review_id=review_id)
    if review_db.student_id != student_id:
        raise Exception

    db.delete(review_db)
    db.commit()


def get(db: Session, review_id: int):
    review_db = db.query(Schema.Review).filter(Schema.Review.id == review_id).first()
    if review_db is None:
        raise Exception

    return ReviewModel.Review.from_orm(review_db)


def get_all_by_course(db: Session, course_id: int):
    return [
        ReviewModel.Review.from_orm(review_db)
        for review_db in db.query(Schema.Review)
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
    ]


def update(db: Session, review_update: ReviewModel.ReviewUpdate, student_id: str):
    review = get(db, review_id=review_update.id)
    if review.student_id != student_id:
        raise Exception

    setattr(review, "updated_at", date.today())
    for attr, value in review_update:
        if value is not None:
            setattr(review, attr, value)

    db.commit()
    db.refresh(review)

    return review
