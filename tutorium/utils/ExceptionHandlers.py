from fastapi import Request
from fastapi.responses import JSONResponse

from .Exceptions import BadRequestException, NotFoundException, UnauthorizedException


def bad_request_exception_handler(request: Request, exc: BadRequestException):
    return JSONResponse(
        status_code=400,
        content={
            "entity": exc.entity,
            "id": exc.id,
            "operation": exc.operation,
            "message": exc.message,
        },
    )


def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={
            "entity": exc.entity,
            "id": exc.id,
            "message": exc.message,
        },
    )


def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=401,
        content={
            "user_id": exc.user_id,
            "message": exc.message,
        },
    )
