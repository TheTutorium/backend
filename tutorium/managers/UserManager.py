import math
from datetime import date, datetime

from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import BookingManager
from ..models import ReviewModel, UserModel
from ..utils import Updater
from ..utils.Exceptions import BadRequestException, NotFoundException


def create(db: Session, user_create: UserModel.UserCreate):
    user_db = Schema.User(
        **user_create.dict(),
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(user_db)
    db.flush()
    return UserModel.User.from_orm(user_db)


def delete(db: Session, user_id: str):
    user_db = get(db, user_id=user_id, as_db=True)
    db.delete(user_db)
    db.flush()


def get(db: Session, user_id: str, as_db: bool = False):
    user_db = db.query(Schema.User).filter(Schema.User.id == user_id).first()
    if user_db is None:
        raise NotFoundException(entity="user", id=user_id)

    return user_db if as_db else UserModel.User.from_orm(user_db)


def get_all_reviews_of_tutor(db: Session, tutor_id: str):
    booking_ids = [
        booking.id for booking in BookingManager.get_all_by_user(db, user_id=tutor_id)
    ]
    reviews_db = (
        db.query(Schema.Review).filter(Schema.Review.booking_id.in_(booking_ids)).all()
    )
    return list(map(ReviewModel.Review.from_orm, reviews_db))


def get_all_tutors(db: Session, as_dict: bool = False):
    tutors_db = db.query(Schema.User).filter(Schema.User.is_tutor).all()
    tutors = list(map(UserModel.User.from_orm, tutors_db))
    return {tutor.id: tutor for tutor in tutors} if as_dict else tutors


def get_hours_given_of_tutor(db: Session, tutor_id: str):
    bookings = BookingManager.get_all_by_user(db, user_id=tutor_id)
    past_booking_durations = [
        booking.duration for booking in bookings if booking.start_time < datetime.now()
    ]
    return math.ceil(sum(past_booking_durations) / 60)


def get_rating_of_tutor(db: Session, tutor_id: str):
    ratings = [
        review.rating for review in get_all_reviews_of_tutor(db, tutor_id=tutor_id)
    ]
    if len(ratings) == 0:
        return -1
    return round(sum(ratings) / len(ratings), 1)


def is_tutor(db: Session, user_id: str):
    user = get(db, user_id=user_id)
    return user.is_tutor


def update(db: Session, user_id: str, user_update: UserModel.UserUpdate):
    _update_checks(user_update)

    user_db = get(db, user_id=user_id, as_db=True)
    Updater.update(user_db, user_update)
    db.flush()
    return UserModel.User.from_orm(user_db)


def _update_checks(user_update: UserModel.UserUpdate):
    if user_update.description and len(user_update.description) < 10:
        raise BadRequestException(
            entity="review",
            id="",
            operation="POST|UPDATE",
            custom_message=f"User description cannot be smaller than ten characters. Given description: {user_update.description}",
        )
