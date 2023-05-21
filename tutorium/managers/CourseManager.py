import os
from datetime import date

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import Schema
from ..managers import BookingManager
from ..models import CourseModel
from ..utils import FileUtils, Updater
from ..utils.ExceptionHandlers import BadRequestException, NotFoundException


def create(db: Session, course_create: CourseModel.CourseCreate, tutor_id: str):
    _create_update_checks(course=course_create)

    course_db = Schema.Course(
        **course_create.dict(),
        created_at=date.today(),
        tutor_id=tutor_id,
        updated_at=date.today(),
    )
    db.add(course_db)
    db.flush()
    return CourseModel.Course.from_orm(course_db)


def deactivate(db: Session, course_id: int):
    course_db = get(db, course_id=course_id, as_db=True)
    setattr(course_db, "deactivated", True)
    setattr(course_db, "updated_at", date.today())
    db.flush()


def delete_picture(db: Session, course_id: int):
    course_db = get(db, course_id=course_id, as_db=True)
    picture_path = course_db.picture_path
    setattr(course_db, "picture_path", None)
    setattr(course_db, "updated_at", date.today())
    db.flush()
    FileUtils.delete_file(picture_path)


def download_picture(db: Session, course_id: int):
    course_db = get(db, course_id=course_id)
    return FileResponse(
        path=course_db.picture_path, filename=os.path.basename(course_db.picture_path)
    )


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


def update(db: Session, course_update: CourseModel.CourseUpdate):
    _create_update_checks(course=course_update)

    course_db = get(db, course_id=course_update.id, as_db=True)
    Updater.update(course_db, course_update)
    db.flush()
    return CourseModel.Course.from_orm(course_db)


def update_picture(db: Session, course_id: int, file: UploadFile):
    course_db = get(db, course_id=course_id, as_db=True)
    if course_db.picture_path:
        delete_picture(db, course_id=course_db.id)

    path = f"courses/{course_id}/{file.filename}"
    setattr(course_db, "picture_path", path)
    setattr(course_db, "updated_at", date.today())
    db.flush()
    FileUtils.save_file(file=file, path=path)

    return path


def is_user_in_course(db: Session, course_id: int, user_id: str):
    return is_tutor_in_course(
        db, course_id=course_id, tutor_id=user_id
    ) or _is_student_in_course(db, course_id=course_id, student_id=user_id)


def is_tutor_in_course(db: Session, course_id: int, tutor_id: str):
    course_db = get(db, course_id=course_id)
    return tutor_id == course_db.tutor_id


def _is_student_in_course(db: Session, course_id: int, student_id: str):
    bookings = BookingManager.get_all_by_user(db, user_id=student_id)
    return course_id in set(booking.course_id for booking in bookings)


def _create_update_checks(course: CourseModel.CourseCreate | CourseModel.CourseUpdate):
    if course.description and len(course.description) < 10:
        raise BadRequestException(
            entity="course",
            id="",
            operation="POST",
            custom_message=f"Course description cannot be smaller than ten characters. Given description: {course.description}",
        )
    if course.duration is not None and course.duration < 10:
        raise BadRequestException(
            entity="course",
            id="",
            operation="POST|UPDATE",
            custom_message=f"Course duration cannot be smaller than ten minutes. Given duration: {course.duration}",
        )
    if course.name and len(course.name) < 5:
        raise BadRequestException(
            entity="course",
            id="",
            operation="POST|UPDATE",
            custom_message=f"Course name cannot be smaller than five characters. Given ame: {course.name}",
        )
