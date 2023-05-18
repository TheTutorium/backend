from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Enum, Integer,
                        String, Time)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .Database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    description = Column(String(255), nullable=True)
    is_tutor = Column(Boolean, default=False)
    profile_pic = Column(String(255), nullable=True)
    created_at = Column(Date)
    updated_at = Column(Date)


class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(String(255))  # No ForeignKey here
    availability = Column(JSON, nullable=False)


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    tutor_id = Column(String(255))  # No ForeignKey here
    start_time = Column(DateTime(timezone=True), default=func.now())
    end_time = Column(DateTime(timezone=True), default=func.now())
