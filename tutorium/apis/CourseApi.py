from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import CourseManager
from ..models import CourseModel
from ..utils.Middleware import authenticate

course_api_router = APIRouter(prefix="/courses", tags=["courses"])


@course_api_router.post("/", response_model=CourseModel.CourseRead)
async def create(
    course_create: CourseModel.CourseCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return CourseManager.create(db, course_create=course_create, tutor_id=user_id)


@course_api_router.delete("/{course_id}/")
async def delete(
    course_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return CourseManager.delete(db, course_id=course_id, tutor_id=user_id)


@course_api_router.get("/all/", response_model=list[CourseModel.CourseRead])
def get_all(
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    courses = CourseManager.get_all(db)
    return courses


@course_api_router.get(
    "/all-by-tutor/{tutor_id}", response_model=list[CourseModel.CourseRead]
)
def get_all_by_tutor(
    tutor_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    courses = CourseManager.get_all_by_tutor(db, tutor_id=tutor_id)
    return courses


@course_api_router.get("/{course_id}/", response_model=CourseModel.CourseRead)
def get(
    course_id: int,
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    course = CourseManager.get(db, course_id=course_id)
    return course
