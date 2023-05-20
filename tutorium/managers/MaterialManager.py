import os
from datetime import date

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import Schema
from ..models import MaterialModel
from . import CourseManager, UserManager


def create(
    db: Session,
    file: UploadFile,
    material_create: MaterialModel.MaterialCreate,
    tutor_id: str,
):
    if not CourseManager.does_tutor_own_course(
        db, course_id=material_create.course_id, tutor_id=tutor_id
    ):
        raise Exception

    name = f"{material_create.name}{_get_extension(file.filename)}"

    material_db = Schema.Material(
        created_at=date.today(),
        course_id=material_create.course_id,
        name=name,
        path="NA",
    )
    db.add(material_db)
    db.commit()
    db.refresh(material_db)

    path = f"materials/{material_db.course_id}/{material_db.id}"
    _save_file(file=file, path=path)

    setattr(material_db, "path", path)
    db.commit()
    db.refresh(material_db)

    return MaterialModel.Material.from_orm(material_db)


def delete(db: Session, material_id: int, tutor_id: str):
    if not UserManager.is_tutor(db, user_id=tutor_id):
        raise Exception

    material_db = get(db, material_id=material_id, user_id=tutor_id)
    db.delete(material_db)
    db.commit()


def download(db: Session, material_id: int, user_id: str):
    material_db = get(db, material_id=material_id, user_id=user_id)
    return FileResponse(material_db.path, filename=material_db.name)


def get(db: Session, material_id: int, user_id: str):
    material_db = (
        db.query(Schema.Material).filter(Schema.Material.id == material_id).first()
    )
    if material_db is None:
        raise Exception

    material = MaterialModel.Material.from_orm(material_db)
    if not CourseManager.does_tutor_own_course(
        db, course_id=material.course_id, tutor_id=user_id
    ) and not CourseManager.is_student_in_course(
        db, course_id=material.course_id, student_id=user_id
    ):
        raise Exception

    return material


def get_all_by_course(db: Session, course_id: int, user_id: str):
    if not CourseManager.does_tutor_own_course(
        db, course_id=course_id, tutor_id=user_id
    ) and not CourseManager.is_student_in_course(
        db, course_id=course_id, student_id=user_id
    ):
        raise Exception

    materials_db = (
        db.query(Schema.Material).filter(Schema.Material.course_id == course_id).all()
    )
    return [
        MaterialModel.Material.from_orm(material_db) for material_db in materials_db
    ]


def _get_extension(filename: str | None):
    return (
        f".{filename.split('.')[-1].lower()}"
        if filename is not None and "." in filename
        else ""
    )


def _save_file(file: UploadFile, path: str):
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)

    with open(path, "wb") as f:
        contents = file.file.read()
        f.write(contents)
