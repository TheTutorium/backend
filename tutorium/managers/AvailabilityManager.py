from datetime import datetime, time

from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..database import Schema
from ..models import AvaibilityModel


def get_availability(db: Session, availability_id: int):
    return (
        db.query(Schema.Availability)
        .filter(Schema.Availability.id == availability_id)
        .first()
    )


def get_availabilities(db: Session, tutor_id: str):
    return (
        db.query(Schema.Availability)
        .filter(Schema.Availability.tutor_id == tutor_id)
        .all()
    )


def create_availability(db: Session, availability: AvaibilityModel.AvailabilityCreate):
    db_availability = Schema.Availability(**availability.dict())
    db.add(db_availability)
    db.commit()
    db.refresh(db_availability)
    return db_availability


def check_availability(db: Session, tutor_id: str, datetime_instance: datetime):
    day = datetime_instance.strftime("%A")
    time_to_check = datetime_instance.time()

    availability = get_availabilities(db, tutor_id)
    filtered_day = [slot for slot in availability.availability if slot["day"] == day]
    if not filtered_day:
        raise HTTPException(status_code=404, detail=f"No availability found for {day}")

    time_slots = filtered_day[0].get("time_slots", [])

    # Filter time slots based on the desired time
    filtered_time_slots = []
    for slot in time_slots:
        start_time = datetime.strptime(slot["start_time"], "%H:%M").time()
        end_time = datetime.strptime(slot["end_time"], "%H:%M").time()
        if start_time <= time_to_check <= end_time:
            filtered_time_slots.append(slot)

    if not filtered_time_slots:
        raise HTTPException(
            status_code=404,
            detail=f"No available time slots found for {day} at {time_to_check}",
        )

    return filtered_time_slots
