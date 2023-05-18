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
    tutor_id: str


class AvailabilityCreate(AvailabilityBase):
    availability: List[AvailabilityDay]


class Availability(AvailabilityBase):
    id: int
    availability: List[AvailabilityDay]

    class Config:
        orm_mode = True
