from enum import Enum
from typing import List

from pydantic import BaseModel


class Day(str, Enum):
    Monday = "Monday"
    Tuesday = "Tuesday"
    Wednesday = "Wednesday"
    Thursday = "Thursday"
    Friday = "Friday"
    Saturday = "Saturday"
    Sunday = "Sunday"


class Time(BaseModel):
    hour: int
    minute: int


class TimeSlot(BaseModel):
    start_time: Time
    end_time: Time


class AvailabilityDay(BaseModel):
    day: Day
    time_slots: List[TimeSlot]


class AvailabilityBase(BaseModel):
    availability: List[AvailabilityDay]


class Availability(AvailabilityBase):
    id: int
    tutor_id: str

    class Config:
        orm_mode = True


class AvailabilityCreate(AvailabilityBase):
    pass


class AvailabilityRead(Availability):
    pass
