from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import CourseModel
from . import UserManager


def create(db: Session, course_create: CourseModel.CourseCreate, tutor_id: str):
    assert UserManager.is_tutor(db, user_id=tutor_id)

    course = Schema.Course(
        **course_create.dict(),
        created_at=date.today(),
        tutor_id=tutor_id,
        updated_at=date.today(),
    )
    db.add(course)
    db.commit()
    db.refresh(course)
    return course


def get(db: Session, course_id: int):
    return db.query(Schema.Course).filter(Schema.Course.id == course_id).first()


def get_all(db: Session):
    return db.query(Schema.Course).all()


def get_all_of_tutor(db: Session, tutor_id: str):
    assert UserManager.is_tutor(db, user_id=tutor_id)

    return db.query(Schema.Course).filter(Schema.Course.tutor_id == tutor_id).all()
