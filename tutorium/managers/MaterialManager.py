from datetime import date

from sqlalchemy.orm import Session

from ..database import Schema
from ..models import MaterialModel
from . import CourseManager, UserManager


def create(db: Session, material_create: MaterialModel.MaterialCreate, tutor_id: str):
    if not CourseManager.does_tutor_own_course(
        db, course_id=material_create.course_id, tutor_id=tutor_id
    ):
        raise Exception

    # TODO

    material = Schema.Material(
        **material_create.dict(),
        created_at=date.today(),
        path="",
    )
    db.add(material)
    db.commit()
    db.refresh(material)
    return material


def delete(db: Session, material_id: int, tutor_id: str):
    if not UserManager.is_tutor(db, user_id=tutor_id):
        raise Exception

    material = get(db, material_id=material_id, user_id=tutor_id)
    db.delete(material)
    db.commit()


def download(db: Session, material_id: int, user_id: str):
    material = get(db, material_id=material_id, user_id=user_id)

    # TODO


def get(db: Session, material_id: int, user_id: str):
    material = (
        db.query(Schema.Material).filter(Schema.Material.id == material_id).first()
    )
    if material is None:
        raise Exception

    course_id = int(material.course_id)
    if not CourseManager.does_tutor_own_course(
        db, course_id=course_id, tutor_id=user_id
    ) and not CourseManager.does_student_in_course(
        db, course_id=course_id, student_id=user_id
    ):
        raise Exception

    return material


def get_all_by_course(db: Session, course_id: int, user_id: str):
    if not CourseManager.does_tutor_own_course(
        db, course_id=course_id, tutor_id=user_id
    ) and not CourseManager.does_student_in_course(
        db, course_id=course_id, student_id=user_id
    ):
        raise Exception

    materials = (
        db.query(Schema.Material).filter(Schema.Material.course_id == course_id).all()
    )
    return materials
