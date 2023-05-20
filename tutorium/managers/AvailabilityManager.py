from sqlalchemy.orm import Session

from ..database import Schema
from ..models import AvailabilityModel


def create(
    db: Session,
    availability_create: AvailabilityModel.AvailabilityCreate,
    tutor_id: str,
):
    availability_db = Schema.Availability(
        **availability_create.dict(), tutor_id=tutor_id
    )
    db.add(availability_db)
    db.commit()
    db.refresh(availability_db)

    return AvailabilityModel.Availability.from_orm(availability_db)


def get_all_by_tutor(db: Session, tutor_id: str):
    availabilities_db = (
        db.query(Schema.Availability)
        .filter(Schema.Availability.tutor_id == tutor_id)
        .all(),
    )
    return list(map(AvailabilityModel.Availability.from_orm, availabilities_db))  # TODO
