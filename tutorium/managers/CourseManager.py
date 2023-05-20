from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import CourseModel
from . import UserManager


def create(db: Session, course_create: CourseModel.CourseCreate, tutor_id: str):
    if not UserManager.is_tutor(db, user_id=tutor_id):
        raise Exception

    course_db = Schema.Course(
        **course_create.dict(),
        created_at=date.today(),
        tutor_id=tutor_id,
        updated_at=date.today(),
    )
    db.add(course_db)
    db.commit()
    db.refresh(course_db)
    return CourseModel.Course.from_orm(course_db)


def delete(db: Session, course_id: int, tutor_id: str):
    course_db = get(db, course_id=course_id, as_db=True)
    if course_db.tutor_id != tutor_id:
        raise Exception

    db.delete(course_db)
    db.commit()


def get(db: Session, course_id: int, as_db: bool = False):
    course_db = db.query(Schema.Course).filter(Schema.Course.id == course_id).first()
    if course_db is None:
        raise Exception

    return course_db if as_db else CourseModel.Course.from_orm(course_db)


def get_all(db: Session):
    return [
        CourseModel.Course.from_orm(course_db)
        for course_db in db.query(Schema.Course).all()
    ]


def get_all_by_tutor(db: Session, tutor_id: str):
    return [
        CourseModel.Course.from_orm(course_db)
        for course_db in db.query(Schema.Course)
        .filter(Schema.Course.tutor_id == tutor_id)
        .all()
    ]


def does_tutor_own_course(db: Session, course_id: int, tutor_id: str):
    course_db = get(db, course_id=course_id)
    return tutor_id == course_db.tutor_id


def is_student_in_course(db: Session, course_id: int, student_id: str):
    pass  # TODO
