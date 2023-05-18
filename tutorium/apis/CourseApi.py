from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import CourseManager
from ..models import CourseModel
from ..utils.Middleware import authenticate

course_api_router = APIRouter(prefix="/courses", tags=["courses"])


@course_api_router.post("/")
async def create(
    course: CourseModel.CourseCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return CourseManager.create_course(db, course=course, user_id=user_id)


@course_api_router.get("/", response_model=list[CourseModel.CourseRead])
def read_all(
    db: Session = Depends(get_db),
    _: Any = Depends(authenticate),
):
    courses = CourseManager.get_courses(db)
    return courses


@course_api_router.get("/courses-of-tutor", response_model=list[CourseModel.CourseRead])
def read_courses_of_tutor(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    courses = CourseManager.get_courses_of_tutor(db, user_id=user_id)
    return courses
