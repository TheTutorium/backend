from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import ReviewManager
from ..models import ReviewModel
from ..utils.Middleware import authenticate

review_api_router = APIRouter(prefix="/reviews", tags=["reviews"])


@review_api_router.post("/", response_model=ReviewModel.ReviewRead)
async def create(
    review_create: ReviewModel.ReviewCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return ReviewManager.create(db, review_create=review_create, student_id=user_id)


@review_api_router.get(
    "/by-course/{course_id}/", response_model=list[ReviewModel.ReviewRead]
)
def get_all_of_course(
    course_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    reviews = ReviewManager.get_all_of_course(db, course_id=course_id)
    return reviews
