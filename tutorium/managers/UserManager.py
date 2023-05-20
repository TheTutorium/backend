from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import UserModel


def create(db: Session, user_create: UserModel.UserCreate):
    user_db = Schema.User(
        **user_create.dict(),
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(user_db)
    db.commit()
    db.refresh(user_db)

    return UserModel.User.from_orm(user_db)


def get(db: Session, user_id: str):
    user_db = db.query(Schema.User).filter(Schema.User.id == user_id).first()
    if user_db is None:
        raise Exception

    return UserModel.User.from_orm(user_db)


def get_all_tutors(db: Session, as_dict: bool = False):
    tutors_db = db.query(Schema.User).filter(Schema.User.is_tutor).all()
    tutors = [UserModel.User.from_orm(tutor_db) for tutor_db in tutors_db]

    return {tutor.id: tutor for tutor in tutors} if as_dict else tutors


def is_tutor(db: Session, user_id: str):
    user = get(db, user_id=user_id)
    return user.is_tutor


def update(db: Session, user_id: str, user_update: UserModel.UserUpdate):
    user = get(db, user_id=user_id)
    assert user is not None

    setattr(user, "updated_at", date.today())
    for attr, value in user_update:
        if value is not None:
            setattr(user, attr, value)

    db.commit()
    db.refresh(user)

    return user
