from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import BookingManager
from ..models import BookingModel
from ..utils.Middleware import authenticate

booking_api_router = APIRouter(prefix="/bookings", tags=["bookings"])


@booking_api_router.post("/", response_model=BookingModel.BookingRead)
async def create(
    booking_create: BookingModel.BookingCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return BookingManager.create(db, booking_create=booking_create, student_id=user_id)


@booking_api_router.get("/all-by-user/", response_model=list[BookingModel.BookingRead])
def get_all_by_user(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    bookings = BookingManager.get_all_by_user(db, user_id=user_id)
    return bookings


@booking_api_router.delete("/{booking_id}")
async def delete(
    booking_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return BookingManager.delete(db, booking_id=booking_id, user_id=user_id)
