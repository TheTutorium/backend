from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..database import Schemas
from ..models import CalModel
from .AvaManager import check_availability


def get_event(db: Session, event_id: int):
    return db.query(Schemas.Event).filter(Schemas.Event.id == event_id).first()  # type: ignore


def get_events(db: Session):
    tutor_id = "user_2PvrGmsFXg61YQWKiLEEiJw88k6"
    return db.query(Schemas.Event).filter(Schemas.Event.tutor_id == tutor_id).all()


def create_event(db: Session, event: CalModel.EventCreate):
    db_event = Schemas.Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


def check_event_conflict(db: Session, event: CalModel.EventCreate):
    events = get_events(db)
    for existing_event in events:
        if (
            existing_event.tutor_id == event.tutor_id
            and existing_event.start_time <= event.start_time <= existing_event.end_time
        ):
            raise HTTPException(status_code=400, detail="Time slot already booked")


def create_event_with_availability_check(db: Session, event: CalModel.EventCreate):
    check_availability(db, event.tutor_id, event.start_time)
    check_availability(db, event.tutor_id, event.end_time)
    check_event_conflict(db, event)
    return create_event(db=db, event=event)
