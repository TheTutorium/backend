from sqlalchemy.orm import Session
from datetime import date

from ..database import Schema
from ..models import ReviewModel


def create_review(db: Session, review: ReviewModel.ReviewCreate):
    db_review = Schema.Review(
        booking_id=review.booking_id,
        comment=review.comment,
        created_at=date.today(),
        rating=review.rating,
        updated_at=date.today(),
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_review(db: Session, review_id: int):
    return db.query(Schema.Review).filter(Schema.Review.id == review_id).first()  # type: ignore


def get_reviews(db: Session):
    return db.query(Schema.Review).all()
