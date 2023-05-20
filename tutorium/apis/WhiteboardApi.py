from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import WhiteboardManager
from ..models import WhiteboardModel
from ..utils.Middleware import authenitcate_tutor, authenticate

whiteboard_api_router = APIRouter(prefix="/whiteboards", tags=["whiteboards"])


@whiteboard_api_router.post("/", response_model=WhiteboardModel.WhiteboardRead)
async def create(
    whiteboard_create: WhiteboardModel.WhiteboardCreate,
    db: Session = Depends(get_db),
    tutor_id: str = Depends(authenitcate_tutor),
):
    return WhiteboardManager.create(
        db, tutor_id=tutor_id, whiteboard_create=whiteboard_create
    )


@whiteboard_api_router.get(
    "/by-booking/{booking_id}/", response_model=WhiteboardModel.WhiteboardRead
)
def get_by_booking_id(
    booking_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return WhiteboardManager.get_by_booking_id(
        db, booking_id=booking_id, user_id=user_id
    )
