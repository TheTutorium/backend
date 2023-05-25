import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from tutorium.apis.AvailabilityApi import availability_api_router
from tutorium.apis.BookingApi import booking_api_router
from tutorium.apis.CourseApi import course_api_router
from tutorium.apis.MaterialApi import material_api_router
from tutorium.apis.ReviewApi import review_api_router
from tutorium.apis.UserApi import user_api_router
from tutorium.apis.WhiteboardApi import whiteboard_api_router
from tutorium.database import Database, Schema
from tutorium.utils.ExceptionHandlers import (
    bad_request_exception_handler,
    not_found_exception_handler,
    unauthorized_exception_handler,
)
from tutorium.utils.Exceptions import (
    BadRequestException,
    NotFoundException,
    UnauthorizedException,
)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(availability_api_router)
app.include_router(booking_api_router)
app.include_router(course_api_router)
app.include_router(material_api_router)
app.include_router(review_api_router)
app.include_router(user_api_router)
app.include_router(whiteboard_api_router)
app.add_exception_handler(BadRequestException, bad_request_exception_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(UnauthorizedException, unauthorized_exception_handler)

Schema.Base.metadata.create_all(bind=Database.engine)


def start():
    uvicorn.run("tutorium.main:app", host="0.0.0.0", port=8000, reload=True)
