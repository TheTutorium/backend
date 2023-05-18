from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import BookingManager
from ..models import BookingModel
from ..utils.Middleware import authenticate

booking_api_router = APIRouter(prefix="/bookings", tags=["bookings"])


@booking_api_router.post("/")
async def create(
    booking: BookingModel.BookingCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return BookingManager.create_booking(db, booking=booking, user_id=user_id)


@booking_api_router.get("/user", response_model=list[BookingModel.BookingRead])
def read_bookings_of_user(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    bookings = BookingManager.get_bookings_of_user(db, user_id=user_id)
    return bookings
