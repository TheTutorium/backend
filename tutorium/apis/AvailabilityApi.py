from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import AvailabilityManager
from ..models import AvaibilityModel
from ..utils.Middleware import authenticate

availibility_api_router = APIRouter(prefix="/availibilities", tags=["availibilities"])


@availibility_api_router.post("/", response_model=AvaibilityModel.AvailabilityRead)
def create(
    availability_create: AvaibilityModel.AvailabilityCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return AvailabilityManager.create(
        db, availability_create=availability_create, tutor_id=user_id
    )


@availibility_api_router.get(
    "/by-tutor/{tutor_id}/", response_model=List[AvaibilityModel.AvailabilityRead]
)
def get_all_of_tutor(
    tutor_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    availabilities = AvailabilityManager.get_all_of_tutor(db, tutor_id=tutor_id)
    return availabilities
