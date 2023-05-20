from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import ReviewManager
from ..models import ReviewModel
from ..utils.Exceptions import UnauthorizedException
from ..utils.Middleware import authenitcate_student, authenticate

review_api_router = APIRouter(prefix="/reviews", tags=["reviews"])


@review_api_router.post("/", response_model=ReviewModel.ReviewRead)
async def create(
    review_create: ReviewModel.ReviewCreate,
    db: Session = Depends(get_db),
    student_id: str = Depends(authenitcate_student),
):
    return ReviewManager.create(db, review_create=review_create, student_id=student_id)


@review_api_router.delete("/{review_id}/")
async def delete(
    review_id: int,
    db: Session = Depends(get_db),
    student_id: str = Depends(authenitcate_student),
):
    if not ReviewManager.does_student_own_review(
        db, review_id=review_id, student_id=student_id
    ):
        raise UnauthorizedException(
            user_id=student_id,
            custom_message=f"Student with id {student_id} does not own this review with id {review_id}",
        )

    ReviewManager.delete(db, review_id=review_id)


@review_api_router.get(
    "/all-by-course/{course_id}/", response_model=list[ReviewModel.ReviewRead]
)
def get_all_by_course(
    course_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    return ReviewManager.get_all_by_course(db, course_id=course_id)


@review_api_router.put("/", response_model=ReviewModel.ReviewRead)
def update(
    review_update: ReviewModel.ReviewUpdate,
    db: Session = Depends(get_db),
    student_id: str = Depends(authenitcate_student),
):
    if not ReviewManager.does_student_own_review(
        db, review_id=review_update.id, student_id=student_id
    ):
        raise UnauthorizedException(
            user_id=student_id,
            custom_message=f"Student with id {student_id} does not own this review with id {review_update.id}",
        )

    return ReviewManager.update(db, review_update=review_update)
