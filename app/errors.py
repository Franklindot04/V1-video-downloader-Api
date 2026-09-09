import logging

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


logger = logging.getLogger(__name__)


def error_response(status_code, message, path):
    return JSONResponse(
        status_code=status_code,
        content={
            "error": {
                "message": message,
                "path": path,
            }
        },
    )


async def http_error_handler(request: Request, exc: HTTPException):
    return error_response(
        status_code=exc.status_code,
        message=str(exc.detail),
        path=request.url.path,
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "message": "Request validation failed.",
                "path": request.url.path,
                "details": exc.errors(),
            }
        },
    )


async def server_error_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled request error",
        extra={
            "method": request.method,
            "path": request.url.path,
        },
    )

    return error_response(
        status_code=500,
        message="Internal server error.",
        path=request.url.path,
    )