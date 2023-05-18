from pydantic import BaseModel
from datetime import time, datetime
from typing import List
from enum import Enum

class DayOfWeek(str, Enum):
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

class EventBase(BaseModel):
    tutor_id: str
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    pass

class Event(EventBase):
    id: int

    class Config:
        orm_mode = True
