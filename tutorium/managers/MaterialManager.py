import os
from datetime import date

from fastapi import UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from ..database import Schema
from ..models import MaterialModel
from ..utils import FileUtils
from ..utils.ExceptionHandlers import BadRequestException, NotFoundException


def create(
    db: Session,
    file: UploadFile,
    material_create: MaterialModel.MaterialCreate,
):
    _create_checks(file=file, material_create=material_create)

    name = f"{material_create.name}{FileUtils.get_extension(file.filename)}"
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
    FileUtils.save_file(file=file, path=path)

    return MaterialModel.Material.from_orm(material_db)


def delete(db: Session, material_id: int):
    material_db = get(db, material_id=material_id, as_db=True)
    db.delete(material_db)
    db.flush()
    FileUtils.delete_file(material_db.path)


def download(db: Session, material_id: int):
    material_db = get(db, material_id=material_id)
    if not os.path.exists(material_db.path):
        sub_db = db.begin().session
        delete(sub_db, material_id=material_id)  # Other deletion handled unproperly.
        sub_db.commit()
        sub_db.close()
        raise NotFoundException(
            entity="material",
            id=material_id,
            custom_message=f"Material with id {material_id} cannot be detected anymore. Please reupload this material. This is an internal error.",
        )

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


def _create_checks(file: UploadFile, material_create: MaterialModel.MaterialCreate):
    if material_create.name and len(material_create.name) < 5:
        raise BadRequestException(
            entity="material",
            id="",
            operation="POST",
            custom_message=f"Material name cannot be smaller than five characters. Description: {material_create.name}",
        )
    if file.size is not None and file.size > 20_000_000:
        BadRequestException(
            entity="material",
            id="",
            operation="POST",
            custom_message="Material size cannot be larger than 20 MB",
        )
