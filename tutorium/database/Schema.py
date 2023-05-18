from sqlalchemy import (JSON, Boolean, Column, Date, DateTime, Integer, String,
                        Text)

from .Database import Base


class Availability(Base):
    __tablename__ = "availabilities"

    id = Column(Integer, primary_key=True)

    availability = Column(JSON)

    tutor_id = Column(String(255))


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True)

    created_at = Column(Date)
    end_time = Column(DateTime)
    start_time = Column(DateTime)
    student_meeting_code = Column(String(15), unique=True)
    tutor_meeting_code = Column(String(15), unique=True)

    course_id = Column(Integer)
    student_id = Column(String(255))


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)

    course_pic = Column(String(255), nullable=True)
    created_at = Column(Date)
    description = Column(String(255))
    duration = Column(Integer)  # In minutes
    name = Column(String(255))
    updated_at = Column(Date)

    tutor_id = Column(String(255))


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True)

    comment = Column(String(255))
    created_at = Column(Date)
    rating = Column(Integer)
    updated_at = Column(Date)

    booking_id = Column(Integer)
    student_id = Column(String(255))


class User(Base):
    __tablename__ = "users"

    id = Column(String(255), primary_key=True)

    created_at = Column(Date)
    description = Column(String(255), default="")
    email = Column(String(255), unique=True)
    first_name = Column(String(255))
    is_tutor = Column(Boolean, default=False)
    last_name = Column(String(255))
    profile_pic = Column(String(255), nullable=True)
    updated_at = Column(Date)


class Whiteboard(Base):
    __tablename__ = "whiteboards"

    id = Column(Integer, primary_key=True)

    content = Column(Text(134217728))
    created_at = Column(DateTime)

    booking_id = Column(Integer)
