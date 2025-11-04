from fastapi import APIRouter, Query, status, HTTPException,Body
from typing import List
from app.models import Unit, UnitCreate, UnitUpdate, UnitStatistics
from app.services import UnitService
from app.exceptions import (
    NotFoundException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    InternalServerException,
    ValidationException
)
from app.schemas.api_examples import (
    UNIT_EXAMPLE,
    UNIT_CREATE_DESCRIPTION,
    UNIT_RESPONSES
)
import logging

router = APIRouter(prefix="/units", tags=["units"])
logger = logging.getLogger(__name__)



@router.post(
    "/",
    response_model=Unit,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new unit",
    description=UNIT_CREATE_DESCRIPTION,
    responses=UNIT_RESPONSES
)
async def create_unit(unit: UnitCreate = Body(..., example=UNIT_EXAMPLE)):
    """Create a new unit"""
    """Create a new unit"""
    try:
        service = UnitService()
        return await service.create_unit(unit)
    except ValueError as e:
        logger.error(f"Validation error while creating unit: {str(e)}")
        raise ValidationException(detail=str(e))
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while creating unit: {str(e)}")
        raise InternalServerException(detail="Failed to create unit")


@router.get("/", response_model=List[Unit])
async def get_units(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return")
):
    """Get all units with pagination"""
    try:
        if skip < 0:
            raise BadRequestException(detail="Skip parameter must be non-negative")
        if limit < 1 or limit > 100:
            raise BadRequestException(detail="Limit must be between 1 and 100")
        
        service = UnitService()
        return await service.get_all_units(skip, limit)
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching units: {str(e)}")
        raise InternalServerException(detail="Failed to fetch units")


@router.get("/{unit_id}", response_model=Unit)
async def get_unit(unit_id: int):
    """Get a specific unit by ID"""
    try:
        if unit_id <= 0:
            raise BadRequestException(detail="Unit ID must be positive")
        
        service = UnitService()
        unit = await service.get_unit(unit_id)
        
        if not unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)
        
        return unit
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching unit {unit_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to fetch unit with id {unit_id}")


@router.put("/{unit_id}", response_model=Unit)
async def update_unit(unit_id: int, unit: UnitUpdate):
    """Update a unit"""
    try:
        if unit_id <= 0:
            raise BadRequestException(detail="Unit ID must be positive")
        
        service = UnitService()
        
        # Check if unit exists
        existing_unit = await service.get_unit(unit_id)
        if not existing_unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)
        
        updated_unit = await service.update_unit(unit_id, unit)
        return updated_unit
    except HTTPException:
        raise
    except ValueError as e:
        logger.error(f"Validation error while updating unit {unit_id}: {str(e)}")
        raise ValidationException(detail=str(e))
    except Exception as e:
        logger.critical(f"Unexpected error while updating unit {unit_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to update unit with id {unit_id}")


@router.delete("/{unit_id}")
async def delete_unit(unit_id: int):
    """Delete a unit"""
    try:
        if unit_id <= 0:
            raise BadRequestException(detail="Unit ID must be positive")
        
        service = UnitService()
        
        # Check if unit exists
        existing_unit = await service.get_unit(unit_id)
        if not existing_unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)
        
        result = await service.delete_unit(unit_id)
        
        return {
            "message": f"Unit with id {unit_id} deleted successfully",
            "deleted_id": unit_id
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while deleting unit {unit_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to delete unit with id {unit_id}")


@router.get("/{unit_id}/statistics", response_model=UnitStatistics)
async def get_unit_statistics(unit_id: int):
    """Get statistics for a specific unit"""
    try:
        if unit_id <= 0:
            raise BadRequestException(detail="Unit ID must be positive")
        
        service = UnitService()
        
        # Check if unit exists
        existing_unit = await service.get_unit(unit_id)
        if not existing_unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)
        
        statistics = await service.get_unit_statistics(unit_id)
        return statistics
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching statistics for unit {unit_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to fetch statistics for unit {unit_id}")