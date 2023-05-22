from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import BookingManager, WhiteboardManager
from ..models import WhiteboardModel
from ..utils.Exceptions import UnauthorizedException
from ..utils.Middleware import authenticate

whiteboard_api_router = APIRouter(prefix="/whiteboards", tags=["whiteboards"])


@whiteboard_api_router.post("/", response_model=WhiteboardModel.WhiteboardRead)
async def create(
    whiteboard_create: WhiteboardModel.WhiteboardCreate,
    db: Session = Depends(get_db),
):
    return WhiteboardManager.create(db, whiteboard_create=whiteboard_create)


@whiteboard_api_router.get(
    "/by-booking/{booking_id}/", response_model=WhiteboardModel.WhiteboardRead
)
def get_by_booking_id(
    booking_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    if not BookingManager.is_user_in_booking(
        db, booking_id=booking_id, user_id=user_id
    ):
        raise UnauthorizedException(
            user_id=user_id,
            custom_message=f"User with id {user_id} is not in this booking with id {booking_id}",
        )

    return WhiteboardManager.get_by_booking_id(db, booking_id=booking_id)
