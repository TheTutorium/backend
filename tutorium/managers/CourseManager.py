from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import CourseModel
from . import UserManager


def create(db: Session, course_create: CourseModel.CourseCreate, tutor_id: str):
    if not UserManager.is_tutor(db, user_id=tutor_id):
        raise Exception

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


def delete(db: Session, course_id: int, tutor_id: str):
    course = get(db, course_id=course_id)
    if course.tutor_id != tutor_id:
        raise Exception

    db.delete(course)
    db.commit()


def get(db: Session, course_id: int):
    course = db.query(Schema.Course).filter(Schema.Course.id == course_id).first()
    if course is None:
        raise Exception

    return course


def get_all(db: Session):
    return db.query(Schema.Course).all()


def get_all_by_tutor(db: Session, tutor_id: str):
    return db.query(Schema.Course).filter(Schema.Course.tutor_id == tutor_id).all()


def does_tutor_own_course(db: Session, course_id: int, tutor_id: str):
    course = get(db, course_id=course_id)
    return course.tutor_id == tutor_id


def does_student_in_course(db: Session, course_id: int, student_id: str):
    pass
