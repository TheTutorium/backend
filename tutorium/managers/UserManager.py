from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import UserModel


def create(db: Session, user_create: UserModel.UserCreate):
    user = Schema.User(
        **user_create.dict(),
        created_at=date.today(),
        updated_at=date.today(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get(db: Session, user_id: str):
    user = db.query(Schema.User).filter(Schema.User.id == user_id).first()
    if user is None:
        raise Exception

    return user


def get_all_tutors(db: Session):
    return db.query(Schema.User).filter(Schema.User.is_tutor).all()


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
