
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, date
from typing import List
from pytz import timezone
from ..database.Database import get_db

from ..database.Database import SessionLocal, engine, Base
from ..models.CalModel import AvailabilityCreate, EventCreate, Availability, Event
from ..managers.AvaManager import get_availability, get_availabilities, create_availability, check_availability
from ..managers.EventManager import get_event, get_events, create_event_with_availability_check

cal_api_router = APIRouter(prefix="/cal" , tags=["cal"])

@cal_api_router.get("/availabilities", response_model=List[Availability])
def read_availabilities(db: Session = Depends(get_db)):
    availabilities = get_availabilities(db, 'user_2PvrGmsFXg61YQWKiLEEiJw88k6')
    return availabilities

@cal_api_router.post("/availabilities", response_model=Availability)
def create_ava(availability: AvailabilityCreate, db: Session = Depends(get_db)):
    return create_availability(db=db, availability=availability)

@cal_api_router.get("/events", response_model=List[Event])
def read_events(db: Session = Depends(get_db)):
    events = get_events(db)
    return events

@cal_api_router.get("/check_availability")
async def check_availability_route(tutor_id: str, datetime_instance: datetime, db: Session = Depends(get_db)):
    return check_availability(db, tutor_id, datetime_instance)

@cal_api_router.post("/events", response_model=Event)
def create_event_route(event: EventCreate, db: Session = Depends(get_db)):
    event.tutor_id = 'user_2PvrGmsFXg61YQWKiLEEiJw88k6'
    return create_event_with_availability_check(db=db, event=event)

@cal_api_router.put("/availabilities/{availability_id}", response_model=Availability)
def update_availability(availability_id: int, availability: AvailabilityCreate, db: Session = Depends(get_db)):
    db_availability = get_availability(db, availability_id)
    if not db_availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    for var, value in vars(availability).items():
        setattr(db_availability, var, value if value else getattr(db_availability, var))
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability