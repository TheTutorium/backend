from typing import Any

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import CourseManager, UserManager
from ..models import CourseModel, UserModel
from ..utils.ExceptionHandlers import UnauthorizedException
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
    return _aggregate(course=course, tutor=tutor)


@course_api_router.post("/deactivate/{course_id}/")
async def deactivate(
    course_id: int,
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    if not CourseManager.is_tutor_in_course(db, course_id=course_id, tutor_id=tutor_id):
        raise UnauthorizedException(
            user_id=tutor_id,
            custom_message=f"Tutor with id {tutor_id} does not own this course with id {course_id}",
        )

    CourseManager.deactivate(db, course_id=course_id)


@course_api_router.get("/{course_id}/picture/")
async def download_picture(
    course_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    return CourseManager.download_picture(db, course_id=course_id)


@course_api_router.get("/all/", response_model=list[CourseModel.CourseRead])
def get_all(
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    courses = CourseManager.get_all(db)
    tutors_dict = UserManager.get_all_tutors(db, as_dict=True)
    return [
        _aggregate(course=course, tutor=tutors_dict.get(course.tutor_id))
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
    return [_aggregate(course=course, tutor=tutor) for course in courses]


@course_api_router.get("/{course_id}/", response_model=CourseModel.CourseRead)
def get(
    course_id: int,
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    course = CourseManager.get(db, course_id=course_id)
    tutor = UserManager.get(db, user_id=course.tutor_id)
    return _aggregate(course=course, tutor=tutor)


@course_api_router.put("/", response_model=CourseModel.CourseRead)
def update(
    course_update: CourseModel.CourseUpdate,
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    if not CourseManager.is_tutor_in_course(
        db, course_id=course_update.id, tutor_id=tutor_id
    ):
        raise UnauthorizedException(
            user_id=tutor_id,
            custom_message=f"Tutor with id {tutor_id} does not own this course with id {course_update.id}",
        )

    course = CourseManager.update(db, course_update=course_update)
    tutor = UserManager.get(db, user_id=course.tutor_id)
    return _aggregate(course=course, tutor=tutor)


@course_api_router.put("/{course_id}/picture", response_model=str)
def update_picture(
    course_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    if not CourseManager.is_tutor_in_course(db, course_id=course_id, tutor_id=tutor_id):
        raise UnauthorizedException(
            user_id=tutor_id,
            custom_message=f"Tutor with id {tutor_id} does not own this course with id {course_id}",
        )

    return CourseManager.update_picture(db, course_id=course_id, file=file)


def _aggregate(course: CourseModel.Course, tutor: UserModel.User):
    return CourseModel.CourseRead(
        **course.dict(),
        tutor_first_name=tutor.first_name,
        tutor_last_name=tutor.last_name,
    )
