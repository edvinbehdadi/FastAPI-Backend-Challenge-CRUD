from fastapi import APIRouter, Query, status, HTTPException, Body
from typing import List, Optional
from app.models import Sensor, SensorCreate, SensorUpdate
from app.services import SensorService
from app.exceptions import (
    NotFoundException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    InternalServerException,
    ValidationException
)
from app.schemas.api_examples import (
    SENSOR_EXAMPLE,
    SENSOR_CREATE_DESCRIPTION,
    SENSOR_RESPONSES
)
import logging

router = APIRouter(prefix="/sensors", tags=["sensors"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=Sensor,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new sensor",
    description=SENSOR_CREATE_DESCRIPTION,
    responses=SENSOR_RESPONSES
)
async def create_sensor(sensor: SensorCreate = Body(..., example=SENSOR_EXAMPLE)):
    """Create a new sensor"""
    try:
        service = SensorService()
        return await service.create_sensor(sensor)
    except ValueError as e:
        logger.error(f"Validation error while creating sensor: {str(e)}")
        raise ValidationException(detail=str(e))
    except NotFoundException as e:
        logger.warning(f"Unit not found while creating sensor: {str(e)}")
        raise NotFoundException(resource_name="Unit", resource_id=sensor.unit_id)
    except ConflictException as e:
        logger.warning(f"Conflict while creating sensor: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while creating sensor: {str(e)}")
        raise
    except HTTPException:
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while creating sensor: {str(e)}")
        raise InternalServerException(detail="Failed to create sensor")

@router.get("/", response_model=List[Sensor])
async def get_sensors(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    unit_id: Optional[int] = Query(None, description="Filter by unit ID")
):
    """Get all sensors with optional filtering by unit_id"""
    try:
        if skip < 0:
            raise BadRequestException(detail="Skip parameter must be non-negative")
        if limit < 1 or limit > 100:
            raise BadRequestException(detail="Limit must be between 1 and 100")
        if unit_id is not None and unit_id <= 0:
            raise BadRequestException(detail="Unit ID must be positive")
        
        service = SensorService()
        return await service.get_all_sensors(skip, limit, unit_id)
    except BadRequestException as e:
        logger.warning(f"Bad request in get_sensors: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while fetching sensors: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching sensors: {str(e)}")
        raise InternalServerException(detail="Failed to fetch sensors")


@router.get("/{sensor_id}", response_model=Sensor)
async def get_sensor(sensor_id: int):
    """Get a specific sensor by ID"""
    try:
        if sensor_id <= 0:
            raise BadRequestException(detail="Sensor ID must be positive")
        
        service = SensorService()
        sensor = await service.get_sensor(sensor_id)
        
        if not sensor:
            raise NotFoundException(resource_name="Sensor", resource_id=sensor_id)
        
        return sensor
    except NotFoundException as e:
        logger.warning(f"Sensor not found: {sensor_id}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in get_sensor: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while fetching sensor {sensor_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching sensor {sensor_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to fetch sensor with id {sensor_id}")


@router.put("/{sensor_id}", response_model=Sensor)
async def update_sensor(sensor_id: int, sensor: SensorUpdate):
    """Update a sensor"""
    try:
        if sensor_id <= 0:
            raise BadRequestException(detail="Sensor ID must be positive")
        
        service = SensorService()
        
        # Check if sensor exists
        existing_sensor = await service.get_sensor(sensor_id)
        if not existing_sensor:
            raise NotFoundException(resource_name="Sensor", resource_id=sensor_id)
        
        # If unit_id is being updated, check if the new unit exists
        if sensor.unit_id is not None and sensor.unit_id != existing_sensor.unit_id:
            from app.services import UnitService
            unit_service = UnitService()
            unit = await unit_service.get_unit(sensor.unit_id)
            if not unit:
                raise NotFoundException(resource_name="Unit", resource_id=sensor.unit_id)
        
        updated_sensor = await service.update_sensor(sensor_id, sensor)
        return updated_sensor
    except NotFoundException as e:
        logger.warning(f"Resource not found for sensor update: {str(e)}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in update_sensor: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Validation error while updating sensor {sensor_id}: {str(e)}")
        raise ValidationException(detail=str(e))
    except ConflictException as e:
        logger.warning(f"Conflict while updating sensor {sensor_id}: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while updating sensor {sensor_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while updating sensor {sensor_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to update sensor with id {sensor_id}")


@router.delete("/{sensor_id}")
async def delete_sensor(sensor_id: int):
    """Delete a sensor"""
    try:
        if sensor_id <= 0:
            raise BadRequestException(detail="Sensor ID must be positive")
        
        service = SensorService()
        
        # Check if sensor exists
        existing_sensor = await service.get_sensor(sensor_id)
        if not existing_sensor:
            raise NotFoundException(resource_name="Sensor", resource_id=sensor_id)
        
        result = await service.delete_sensor(sensor_id)
        
        return {
            "message": f"Sensor with id {sensor_id} deleted successfully",
            "deleted_id": sensor_id
        }
    except NotFoundException as e:
        logger.warning(f"Sensor not found for deletion: {sensor_id}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in delete_sensor: {str(e)}")
        raise
    except ConflictException as e:
        logger.warning(f"Conflict while deleting sensor {sensor_id}: {str(e)}")
        raise ConflictException(detail=f"Cannot delete sensor {sensor_id}. It may have associated sensor data.")
    except DatabaseException as e:
        logger.error(f"Database error while deleting sensor {sensor_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while deleting sensor {sensor_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to delete sensor with id {sensor_id}")