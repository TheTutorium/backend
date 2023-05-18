from sqlalchemy.orm import Session
from datetime import date


from ..database import Schema
from ..models import UserModel


def create_user(db: Session, user: UserModel.UserCreate):
    db_user = Schema.User(
        created_at=date.today(),
        email=user.email,
        first_name=user.first_name,
        id=user.id,
        last_name=user.last_name,
        profile_pic=user.profile_pic,
        updated_at=date.today(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str):
    return db.query(Schema.User).filter(Schema.User.id == user_id).first()  # type: ignore


def get_users(db: Session):
    return db.query(Schema.User).all()


def is_tutor(db: Session, user_id: str):
    return db.query(Schema.User).filter(Schema.User.id == user_id).first().is_tutor  # type: ignore


def update_user(db: Session, user_id: str, user_update: UserModel.UserUpdate):
    user = get_user(db, user_id)
    if user:
        # Modify the desired attributes of the entity
        setattr(user, "updated_at", date.today())
        for attr, value in user_update:
            if value is not None:
                setattr(user, attr, value)

        # Commit the changes to the database
        db.commit()

    return user
