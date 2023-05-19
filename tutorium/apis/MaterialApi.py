from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import MaterialManager
from ..models import MaterialModel
from ..utils.Middleware import authenticate

material_api_router = APIRouter(prefix="/materials", tags=["materials"])


@material_api_router.post("/", response_model=MaterialModel.MaterialRead)
async def create(
    material_create: MaterialModel.MaterialCreate = Depends(),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return MaterialManager.create(
        db, file=file, material_create=material_create, tutor_id=user_id
    )


@material_api_router.delete("/{material_id}/")
async def delete(
    material_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    MaterialManager.delete(db, material_id=material_id, tutor_id=user_id)


@material_api_router.get("/download/{material_id}/")  # TODO
async def download(
    material_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return MaterialManager.download(db, material_id=material_id, user_id=user_id)


@material_api_router.get(
    "/all-by-course/{course_id}/", response_model=list[MaterialModel.MaterialRead]
)
def get_all_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    materials = MaterialManager.get_all_by_course(
        db, course_id=course_id, user_id=user_id
    )
    return materials
