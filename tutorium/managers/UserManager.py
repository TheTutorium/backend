from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import UserModel
from ..utils import Updater
from ..utils.Exceptions import NotFoundException


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


def delete(db: Session, user_id: str):
    user_db = get(db, user_id=user_id, as_db=True)
    db.delete(user_db)
    db.commit()


def get(db: Session, user_id: str, as_db: bool = True):
    user_db = db.query(Schema.User).filter(Schema.User.id == user_id).first()
    if user_db is None:
        raise NotFoundException(entity="user", id=user_id)

    return user_db if as_db else UserModel.User.from_orm(user_db)


def get_all_tutors(db: Session, as_dict: bool = False):
    tutors_db = db.query(Schema.User).filter(Schema.User.is_tutor).all()
    tutors = list(map(UserModel.User.from_orm, tutors_db))
    return {tutor.id: tutor for tutor in tutors} if as_dict else tutors


def is_tutor(db: Session, user_id: str):
    user = get(db, user_id=user_id)
    return user.is_tutor


def update(db: Session, user_id: str, user_update: UserModel.UserUpdate):
    user_db = get(db, user_id=user_id, as_db=True)
    Updater.update(user_db, user_update)
    db.commit()
    db.refresh(user_db)
    return UserModel.User.from_orm(user_db)
