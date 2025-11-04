from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError, OperationalError
from app.exceptions import (
    NotFoundException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    InternalServerException,
    ValidationException
)
import logging

logger = logging.getLogger(__name__)


async def not_found_exception_handler(request: Request, exc: NotFoundException):
    """Handle NotFoundException (404)"""
    logger.warning(f"Not found: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def bad_request_exception_handler(request: Request, exc: BadRequestException):
    """Handle BadRequestException (400)"""
    logger.warning(f"Bad request: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def conflict_exception_handler(request: Request, exc: ConflictException):
    """Handle ConflictException (409)"""
    logger.warning(f"Conflict: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def validation_exception_handler(request: Request, exc: ValidationException):
    """Handle ValidationException (422)"""
    logger.warning(f"Validation error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Validation Error",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def database_exception_handler(request: Request, exc: DatabaseException):
    """Handle DatabaseException (503)"""
    logger.error(f"Database error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={
            "error": "Database Error",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def internal_server_exception_handler(request: Request, exc: InternalServerException):
    """Handle InternalServerException (500)"""
    logger.critical(f"Internal server error: {exc.detail}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle FastAPI RequestValidationError (422)"""
    logger.warning(f"Request validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "Request Validation Error",
            "message": "Invalid request data",
            "details": exc.errors(),
            "path": str(request.url)
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle general HTTP exceptions"""
    logger.warning(f"HTTP exception {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Error",
            "message": exc.detail,
            "path": str(request.url)
        }
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handle SQLAlchemy errors"""
    logger.error(f"SQLAlchemy error: {str(exc)}")
    
    if isinstance(exc, IntegrityError):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": "Database Integrity Error",
                "message": "Operation violates database constraints",
                "path": str(request.url)
            }
        )
    elif isinstance(exc, OperationalError):
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": "Database Connection Error",
                "message": "Could not connect to database",
                "path": str(request.url)
            }
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "Database Error",
                "message": "An error occurred while processing your request",
                "path": str(request.url)
            }
        )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.critical(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": str(request.url)
        }
    )


def register_exception_handlers(app):
    """Register all exception handlers to the FastAPI app"""
    
    # Custom exceptions
    app.add_exception_handler(NotFoundException, not_found_exception_handler)
    app.add_exception_handler(BadRequestException, bad_request_exception_handler)
    app.add_exception_handler(ConflictException, conflict_exception_handler)
    app.add_exception_handler(ValidationException, validation_exception_handler)
    app.add_exception_handler(DatabaseException, database_exception_handler)
    app.add_exception_handler(InternalServerException, internal_server_exception_handler)
    
    # FastAPI built-in exceptions
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    
    # Database exceptions
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    
    # Catch-all for unhandled exceptions
    app.add_exception_handler(Exception, general_exception_handler)
    
    logger.info("All exception handlers registered successfully")
