from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """Exception raised when a resource is not found"""
    def __init__(self, resource_name: str, resource_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource_name} with id {resource_id} not found"
        )


class BadRequestException(HTTPException):
    """Exception raised for bad requests"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )


class ConflictException(HTTPException):
    """Exception raised when there's a conflict"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail
        )


class UnprocessableEntityException(HTTPException):
    """Exception raised when entity cannot be processed"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class InternalServerException(HTTPException):
    """Exception raised for internal server errors"""
    def __init__(self, detail: str = "An internal server error occurred"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class DatabaseException(HTTPException):
    """Exception raised for database errors"""
    def __init__(self, detail: str = "Database operation failed"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )


class ValidationException(HTTPException):
    """Exception raised for validation errors"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )
