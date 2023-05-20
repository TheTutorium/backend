from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import CourseManager, MaterialManager
from ..models import MaterialModel
from ..utils.Exceptions import UnauthorizedException
from ..utils.Middleware import authenitcate_tutor, authenticate

material_api_router = APIRouter(prefix="/materials", tags=["materials"])


@material_api_router.post("/", response_model=MaterialModel.MaterialRead)
async def create(
    file: UploadFile = File(...),
    material_create: MaterialModel.MaterialCreate = Depends(),
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    if not CourseManager.is_tutor_in_course(
        db, course_id=material_create.course_id, tutor_id=tutor_id
    ):
        raise UnauthorizedException(
            user_id=tutor_id,
            custom_message=f"Tutor with id {tutor_id} does not own this course with id {material_create.course_id}",
        )

    return MaterialManager.create(db, file=file, material_create=material_create)


@material_api_router.delete("/{material_id}/")
async def delete(
    material_id: int,
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    material = MaterialManager.get(db, material_id=material_id)
    if not CourseManager.is_tutor_in_course(
        db, course_id=material.course_id, tutor_id=tutor_id
    ):
        raise UnauthorizedException(
            user_id=tutor_id,
            custom_message=f"Tutor with id {tutor_id} does not own this course with id {material.course_id}",
        )

    MaterialManager.delete(db, material_id=material_id)


@material_api_router.get("/download/{material_id}/")
async def download(
    material_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    material = MaterialManager.get(db, material_id=material_id)
    if not CourseManager.is_user_in_course(
        db, course_id=material.course_id, user_id=user_id
    ):
        raise UnauthorizedException(
            user_id=user_id,
            custom_message=f"User with id {user_id} is not in this course with id {material.course_id}",
        )

    return MaterialManager.download(db, material_id=material_id)


@material_api_router.get(
    "/all-by-course/{course_id}/", response_model=list[MaterialModel.MaterialRead]
)
def get_all_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    if not CourseManager.is_user_in_course(db, course_id=course_id, user_id=user_id):
        raise UnauthorizedException(
            user_id=user_id,
            custom_message=f"User with id {user_id} is not in this course with id {course_id}",
        )

    return MaterialManager.get_all_by_course(db, course_id=course_id)
