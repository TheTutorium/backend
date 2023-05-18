from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import AvailabilityManager
from ..models import AvailabilityModel
from ..utils.Middleware import authenticate

availability_api_router = APIRouter(prefix="/availabilities", tags=["availabilities"])


@availability_api_router.post("/", response_model=AvailabilityModel.AvailabilityRead)
def create(
    availability_create: AvailabilityModel.AvailabilityCreate,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    return AvailabilityManager.create(
        db, availability_create=availability_create, tutor_id=user_id
    )


@availability_api_router.get(
    "/all-by-tutor/{tutor_id}/", response_model=List[AvailabilityModel.AvailabilityRead]
)
def get_all_by_tutor(
    tutor_id: str,
    db: Session = Depends(get_db),
    _: str = Depends(authenticate),
):
    availabilities = AvailabilityManager.get_all_by_tutor(db, tutor_id=tutor_id)
    return availabilities
