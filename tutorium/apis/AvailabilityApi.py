from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pytz import timezone
from sqlalchemy.orm import Session

from ..database.Database import Base, SessionLocal, engine, get_db
from ..managers.AvailabilityManager import (
    check_availability,
    create_availability,
    get_availabilities,
    get_availability,
)
from ..models.AvaibilityModel import (
    Availability,
    AvailabilityCreate,
)

cal_api_router = APIRouter(prefix="/cal", tags=["cal"])


@cal_api_router.get("/availabilities", response_model=List[Availability])
def read_availabilities(db: Session = Depends(get_db)):
    availabilities = get_availabilities(db, "user_2PvrGmsFXg61YQWKiLEEiJw88k6")
    return availabilities


@cal_api_router.post("/availabilities", response_model=Availability)
def create_ava(availability: AvailabilityCreate, db: Session = Depends(get_db)):
    return create_availability(db=db, availability=availability)


@cal_api_router.get("/check_availability")
async def check_availability_route(
    tutor_id: str, datetime_instance: datetime, db: Session = Depends(get_db)
):
    return check_availability(db, tutor_id, datetime_instance)


@cal_api_router.put("/availabilities/{availability_id}", response_model=Availability)
def update_availability(
    availability_id: int,
    availability: AvailabilityCreate,
    db: Session = Depends(get_db),
):
    db_availability = get_availability(db, availability_id)
    if not db_availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    for var, value in vars(availability).items():
        setattr(db_availability, var, value if value else getattr(db_availability, var))
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability
