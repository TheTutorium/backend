from sqlalchemy.orm import Session

from ..database import Schemas
from ..models import UserModel


def create_user(db: Session, user: UserModel.UserCreate):
    db_user = Schemas.User(
        created_at=user.created_at,
        email=user.email,
        first_name=user.first_name,
        id=user.id,
        last_name=user.last_name,
        profile_pic=user.profile_pic,
        updated_at=user.updated_at,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: str):
    return db.query(Schemas.User).filter(Schemas.User.id == user_id).first()  # type: ignore


def get_users(db: Session):
    return db.query(Schemas.User).all()


def update_user(db: Session, user_id: str, user_update: UserModel.UserUpdate):
    user = get_user(db, user_id)
    if user:
        # Modify the desired attributes of the entity
        for attr, value in user_update:
            if value is not None:
                setattr(user, attr, value)

        # Commit the changes to the database
        db.commit()

    return user
