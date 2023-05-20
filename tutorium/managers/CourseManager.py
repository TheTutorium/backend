from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import BookingManager
from ..models import CourseModel
from ..utils import Updater
from ..utils.ExceptionHandlers import NotFoundException


def create(db: Session, course_create: CourseModel.CourseCreate, tutor_id: str):
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


def delete(db: Session, course_id: int):
    course_db = get(db, course_id=course_id, as_db=True)
    db.delete(course_db)
    db.commit()


def get(db: Session, course_id: int, as_db: bool = False):
    course_db = db.query(Schema.Course).filter(Schema.Course.id == course_id).first()
    if course_db is None:
        raise NotFoundException(entity="course", id=course_id)

    return course_db if as_db else CourseModel.Course.from_orm(course_db)


def get_all(db: Session, as_dict: bool = False):
    courses = map(CourseModel.Course.from_orm, db.query(Schema.Course).all())
    return {course.id: course for course in courses} if as_dict else list(courses)


def get_all_by_tutor(db: Session, tutor_id: str):
    return list(
        map(
            CourseModel.Course.from_orm,
            db.query(Schema.Course).filter(Schema.Course.tutor_id == tutor_id).all(),
        )
    )


def update(db: Session, course_update: CourseModel.CourseUpdate, tutor_id: str):
    course_db = get(db, course_id=course_update.id, as_db=True)
    Updater.update(course_db, course_update)
    db.commit()
    db.refresh(course_db)
    return CourseModel.Course.from_orm(course_db)


def is_user_in_course(db: Session, course_id: int, user_id: str):
    return is_tutor_in_course(
        db, course_id=course_id, tutor_id=user_id
    ) or _is_student_in_course(db, course_id=course_id, student_id=user_id)


def is_tutor_in_course(db: Session, course_id: int, tutor_id: str):
    course_db = get(db, course_id=course_id)
    return tutor_id == course_db.tutor_id


def _is_student_in_course(db: Session, course_id: int, student_id: str):
    bookings = BookingManager.get_all_by_user(db, user_id=student_id)
    return course_id in [booking.course_id for booking in bookings]
