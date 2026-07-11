# app/core/handlers.py

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.schemas.response import ResponseModel
from app.core.exceptions import AppException

# handle custom exceptions
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            success=False,
            message=exc.message,
            error=str(exc.message)
        ).dict()
    )

# handle http exceptions 
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content=ResponseModel(
            success=False,
            message=exc.detail,
            error=exc.detail
        ).dict()
    )

# handle validation errrors

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content=ResponseModel(
            success=False,
            message="Validation Error",
            error=exc.errors()
        ).dict()
    )

# handle unexpected exceptions
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content=ResponseModel(
            success=False,
            message="Internal Server Error",
            error=str(exc)
        ).dict()
    )