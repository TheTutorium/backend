from sqlalchemy.orm import Session

from ..database import Schema
from ..models import AvailabilityModel
from . import UserManager


def create(
    db: Session,
    availability_create: AvailabilityModel.AvailabilityCreate,
    tutor_id: str,
):
    if not UserManager.is_tutor(db, user_id=tutor_id):
        raise Exception

    availability_db = Schema.Availability(
        **availability_create.dict(), tutor_id=tutor_id
    )
    db.add(availability_db)
    db.commit()
    db.refresh(availability_db)

    return AvailabilityModel.Availability.from_orm(availability_db)


def get_all_by_tutor(db: Session, tutor_id: str):
    return [
        AvailabilityModel.Availability.from_orm(availability_db)
        for availability_db in db.query(Schema.Availability)
        .filter(Schema.Availability.tutor_id == tutor_id)
        .all()
    ]
