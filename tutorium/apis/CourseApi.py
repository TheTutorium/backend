from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import CourseManager, UserManager
from ..models import CourseModel, UserModel
from ..utils.Middleware import authenitcate_tutor, authenticate

course_api_router = APIRouter(prefix="/courses", tags=["courses"])


@course_api_router.post("/", response_model=CourseModel.CourseRead)
async def create(
    course_create: CourseModel.CourseCreate,
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    course = CourseManager.create(db, course_create=course_create, tutor_id=tutor_id)
    tutor = UserManager.get(db, user_id=course.tutor_id)
    return _aggregate_tutor(course=course, tutor=tutor)


@course_api_router.delete("/{course_id}/")
async def delete(
    course_id: int,
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    CourseManager.delete(db, course_id=course_id, tutor_id=tutor_id)


@course_api_router.get("/all/", response_model=list[CourseModel.CourseRead])
def get_all(
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    courses = CourseManager.get_all(db)
    tutors_dict = UserManager.get_all_tutors(db, as_dict=True)
    return [
        _aggregate_tutor(course=course, tutor=tutors_dict.get(course.tutor_id))
        for course in courses
    ]


@course_api_router.get(
    "/all-by-tutor/{tutor_id}", response_model=list[CourseModel.CourseRead]
)
def get_all_by_tutor(
    tutor_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    courses = CourseManager.get_all_by_tutor(db, tutor_id=tutor_id)
    tutor = UserManager.get(db, user_id=tutor_id)
    return [_aggregate_tutor(course=course, tutor=tutor) for course in courses]


@course_api_router.get("/{course_id}/", response_model=CourseModel.CourseRead)
def get(
    course_id: int,
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    course = CourseManager.get(db, course_id=course_id)
    tutor = UserManager.get(db, user_id=course.tutor_id)
    return _aggregate_tutor(course=course, tutor=tutor)


def _aggregate_tutor(course: CourseModel.Course, tutor: UserModel.User):
    return CourseModel.CourseRead(
        **course.dict(),
        tutor_first_name=tutor.first_name,
        tutor_last_name=tutor.last_name
    )
