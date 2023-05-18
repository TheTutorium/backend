from sqlalchemy.orm import Session
from datetime import date

from ..database import Schema
from ..models import CourseModel
from . import UserManager


def create_course(db: Session, course: CourseModel.CourseCreate, user_id: str):
    assert UserManager.is_tutor(db, user_id=user_id)

    db_course = Schema.Course(
        created_at=date.today(),
        description=course.description,
        duration=course.duration,
        name=course.name,
        tutor_id=user_id,
        updated_at=date.today(),
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def get_courses_of_tutor(db: Session, user_id: str):
    return db.query(Schema.Course).filter(Schema.Course.tutor_id == user_id).all()


def get_courses(db: Session):
    return db.query(Schema.Course).all()
