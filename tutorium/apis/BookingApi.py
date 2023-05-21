from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database.Database import get_db
from ..managers import BookingManager, CourseManager, UserManager
from ..models import BookingModel, CourseModel, UserModel
from ..utils.Exceptions import UnauthorizedException
from ..utils.Middleware import authenitcate_student, authenticate

booking_api_router = APIRouter(prefix="/bookings", tags=["bookings"])


@booking_api_router.post("/", response_model=BookingModel.BookingRead)
async def create(
    booking_create: BookingModel.BookingCreate,
    db: Session = Depends(get_db),
    student_id: str = Depends(authenitcate_student),
):
    # TODO
    booking = BookingManager.create(
        db, booking_create=booking_create, student_id=student_id
    )
    course = CourseManager.get(db, course_id=booking.course_id)
    tutor = UserManager.get(db, user_id=course.tutor_id)
    return _aggregate(booking=booking, course=course, tutor=tutor)


@booking_api_router.delete("/{booking_id}/")
async def delete(
    booking_id: int,
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    if not BookingManager.is_user_in_booking(
        db, booking_id=booking_id, user_id=user_id
    ):
        raise UnauthorizedException(
            user_id=user_id,
            custom_message=f"User with id {user_id} is not a participant of this booking with id {booking_id}.",
        )

    BookingManager.delete(db, booking_id=booking_id)


@booking_api_router.get("/all-by-user/", response_model=list[BookingModel.BookingRead])
def get_all_by_user(
    db: Session = Depends(get_db),
    user_id: str = Depends(authenticate),
):
    bookings = BookingManager.get_all_by_user(db, user_id=user_id)
    courses = CourseManager.get_all(db, as_dict=True)
    tutors = UserManager.get_all_tutors(db, as_dict=True)
    return [
        _aggregate(
            booking=booking,
            course=courses.get(booking.course_id),
            tutor=tutors.get(courses.get(booking.course_id).tutor_id),
        )
        for booking in bookings
    ]


def _aggregate(
    booking: BookingModel.Booking, course: CourseModel.Course, tutor: UserModel.User
):
    return BookingModel.BookingRead(
        **booking.dict(),
        course_description=course.description,
        course_duration=course.duration,
        course_name=course.name,
        course_pic=course.course_pic,
        tutor_first_name=tutor.first_name,
        tutor_id=tutor.id,
        tutor_last_name=tutor.last_name,
    )
