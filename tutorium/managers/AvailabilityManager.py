from sqlalchemy.orm import Session

from ..database import Schema
from ..models import AvailabilityModel
from . import UserManager


def create(
    db: Session,
    availability_create: AvailabilityModel.AvailabilityCreate,
    tutor_id: str,
):
    assert UserManager.is_tutor(db, user_id=tutor_id)

    availability = Schema.Availability(**availability_create.dict(), tutor_id=tutor_id)
    db.add(availability)
    db.commit()
    db.refresh(availability)
    return availability


def get_all_of_tutor(db: Session, tutor_id: str):
    assert UserManager.is_tutor(db, user_id=tutor_id)

    return (
        db.query(Schema.Availability)
        .filter(Schema.Availability.tutor_id == tutor_id)
        .all()
    )
