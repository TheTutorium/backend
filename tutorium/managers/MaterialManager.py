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

    material = Schema.Material(
        created_at=date.today(),
        course_id=material_create.course_id,
        name=name,
        path="NA",
    )
    db.add(material)
    db.commit()
    db.refresh(material)

    path = f"materials/{material.course_id}/{material.id}"
    _save_file(file=file, path=path)

    setattr(material, "path", path)
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
    return FileResponse(material.path, filename=material.name)


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
