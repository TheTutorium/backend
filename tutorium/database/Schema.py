from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    DateTime,
    Integer,
    String,
)

from .Database import Base


class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True, index=True)

    availability = Column(JSON, nullable=False)

    tutor_id = Column(String(255))


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)

    end_time = Column(DateTime)
    start_time = Column(DateTime)

    course_id = Column(Integer)


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)

    created_at = Column(Date)
    description = Column(String(255), nullable=True)
    duration = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True)
    updated_at = Column(Date)

    tutor_id = Column(Integer)


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    comment = Column(String(255), nullable=True)
    created_at = Column(Date)
    rating = Column(Integer, primary_key=True)
    updated_at = Column(Date)

    booking_id = Column(Integer)


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)

    description = Column(String(255), nullable=True)
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    is_tutor = Column(Boolean, default=False)
    last_name = Column(String(255))
    profile_pic = Column(String(255), nullable=True)
    created_at = Column(Date)
    updated_at = Column(Date)


class Whiteboard(Base):
    __tablename__ = "whiteboards"

    id = Column(Integer, primary_key=True)

    content = Column(String(134217728), nullable=True)
    created_at = Column(DateTime)
    rating = Column(Integer, primary_key=True)

    booking_id = Column(Integer)
