from enum import Enum
from typing import List

from pydantic import BaseModel


class DAYS(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class TimeSlot(BaseModel):
    start_time: str
    end_time: str


class AvailabilityDay(BaseModel):
    day: str
    time_slots: List[TimeSlot]


class AvailabilityBase(BaseModel):
    availability: List[AvailabilityDay]


class Availability(AvailabilityBase):
    availability: List[AvailabilityDay]
    id: int
    tutor_id: str

    class Config:
        orm_mode = True


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityRead(Availability):
    pass
