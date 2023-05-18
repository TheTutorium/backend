from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import WhiteboardManager
from ..models import WhiteboardModel
from ..utils.Middleware import authenticate

whiteboard_api_router = APIRouter(prefix="/whiteboards", tags=["whiteboards"])


@whiteboard_api_router.post("/", response_model=WhiteboardModel.WhiteboardRead)
async def create(
    whiteboard_create: WhiteboardModel.WhiteboardCreate,
    db: Session = Depends(get_db),
    _=Depends(authenticate),
):
    return WhiteboardManager.create(db, whiteboard_create=whiteboard_create)


@whiteboard_api_router.get(
    "/by-booking/{booking_id}/", response_model=WhiteboardModel.WhiteboardRead
)
def get_by_booking_id(
    booking_id: int,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    whiteboard = WhiteboardManager.get_by_booking_id(db, booking_id=booking_id)
    return whiteboard
