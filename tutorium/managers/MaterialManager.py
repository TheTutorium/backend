import os
from datetime import date

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import Schema
from ..models import MaterialModel
from ..utils.ExceptionHandlers import BadRequestException, NotFoundException


def create(
    db: Session,
    file: UploadFile,
    material_create: MaterialModel.MaterialCreate,
):
    _create_checks(material_create=material_create)

    name = f"{material_create.name}{_get_extension(file.filename)}"
    material_db = Schema.Material(
        created_at=date.today(),
        course_id=material_create.course_id,
        name=name,
        path="notAvailable",
    )
    db.add(material_db)
    db.flush()

    path = f"materials/{material_db.course_id}/{material_db.id}"
    setattr(material_db, "path", path)
    db.flush()
    _save_file(file=file, path=path)

    return MaterialModel.Material.from_orm(material_db)


def delete(db: Session, material_id: int):
    material_db = get(db, material_id=material_id, as_db=True)
    db.delete(material_db)
    db.flush()
    _delete_file(material_db.path)


def download(db: Session, material_id: int):
    material_db = get(db, material_id=material_id)
    return FileResponse(material_db.path, filename=material_db.name)


def get(db: Session, material_id: int, as_db: bool = False):
    material_db = (
        db.query(Schema.Material).filter(Schema.Material.id == material_id).first()
    )
    if material_db is None:
        raise NotFoundException(entity="material", id=material_id)

    return material_db if as_db else MaterialModel.Material.from_orm(material_db)


def get_all_by_course(db: Session, course_id: int):
    materials_db = (
        db.query(Schema.Material).filter(Schema.Material.course_id == course_id).all()
    )
    return list(map(MaterialModel.Material.from_orm, materials_db))


def _delete_file(path: str):
    os.remove(path)


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


def _create_checks(material_create: MaterialModel.MaterialCreate):
    if material_create.name and len(material_create.name) < 5:
        raise BadRequestException(
            entity="material",
            id="",
            operation="POST",
            custom_message=f"Material name cannot be smaller than five characters. Description: {material_create.name}",
        )
