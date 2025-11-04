from fastapi import APIRouter, Query, status, HTTPException, Body
from typing import List, Optional
from app.models import SensorData, SensorDataCreate, SensorDataUpdate, DataStatus, SensorDataWithDetails
from app.services import SensorDataService
from app.exceptions import (
    NotFoundException,
    BadRequestException,
    ConflictException,
    DatabaseException,
    InternalServerException,
    ValidationException
)
from app.schemas.api_examples import (
    SENSOR_DATA_EXAMPLE,
    SENSOR_DATA_CREATE_DESCRIPTION,
    SENSOR_DATA_RESPONSES
)

import logging

router = APIRouter(prefix="/sensor-data", tags=["sensor-data"])
logger = logging.getLogger(__name__)


@router.post(
    "/",
    response_model=SensorData,
    status_code=status.HTTP_201_CREATED,
    summary="Create sensor data",
    description=SENSOR_DATA_CREATE_DESCRIPTION,
    responses=SENSOR_DATA_RESPONSES
)
async def create_sensor_data(sensor_data: SensorDataCreate = Body(..., example=SENSOR_DATA_EXAMPLE)):
    """Create a new sensor data entry"""
    try:
        service = SensorDataService()
        return await service.create_sensor_data(sensor_data)
    
    except ValueError as e:
        logger.error(f"Validation error while creating sensor data: {str(e)}")
        raise ValidationException(detail=str(e))
    except HTTPException:  
       raise 
    except NotFoundException as e:
        logger.warning(f"Sensor not found while creating sensor data: {str(e)}")
        raise NotFoundException(resource_name="Sensor", resource_id=sensor_data.sensor_id)
    except ConflictException as e:
        logger.warning(f"Conflict while creating sensor data: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while creating sensor data: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while creating sensor data: {str(e)}")
        raise InternalServerException(detail="Failed to create sensor data")


@router.get("/", response_model=List[SensorData] | List[SensorDataWithDetails])
async def get_sensor_data(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=100, description="Maximum number of records to return"),
    sensor_id: Optional[int] = Query(None, description="Filter by sensor ID"),
    status: Optional[DataStatus] = Query(None, description="Filter by status"),
    with_details: bool = Query(False, description="Include sensor and unit details")
):
    """Get all sensor data with optional filtering"""
    try:
        if skip < 0:
            raise BadRequestException(detail="Skip parameter must be non-negative")
        if limit < 1 or limit > 100:
            raise BadRequestException(detail="Limit must be between 1 and 100")
        if sensor_id is not None and sensor_id <= 0:
            raise BadRequestException(detail="Sensor ID must be positive")
        
        service = SensorDataService()
        return await service.get_all_sensor_data(skip, limit, sensor_id, status, with_details)
    except HTTPException:  
       raise 
    except BadRequestException as e:
        logger.warning(f"Bad request in get_sensor_data: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while fetching sensor data: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching sensor data: {str(e)}")
        raise InternalServerException(detail="Failed to fetch sensor data")


@router.get("/{data_id}", response_model=SensorData)
async def get_sensor_data_by_id(data_id: int):
    """Get a specific sensor data entry by ID"""
    try:
        if data_id <= 0:
            raise BadRequestException(detail="Data ID must be positive")
        
        service = SensorDataService()
        sensor_data = await service.get_sensor_data(data_id)
        
        if not sensor_data:
            raise NotFoundException(resource_name="SensorData", resource_id=data_id)
        
        return sensor_data
    except HTTPException:  
       raise 
    except NotFoundException as e:
        logger.warning(f"Sensor data not found: {data_id}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in get_sensor_data_by_id: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while fetching sensor data {data_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while fetching sensor data {data_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to fetch sensor data with id {data_id}")


@router.put("/{data_id}", response_model=SensorData)
async def update_sensor_data(data_id: int, sensor_data: SensorDataUpdate):
    """Update sensor data"""
    try:
        if data_id <= 0:
            raise BadRequestException(detail="Data ID must be positive")
        
        service = SensorDataService()
        
        # Check if sensor data exists
        existing_data = await service.get_sensor_data(data_id)
        if not existing_data:
            raise NotFoundException(resource_name="SensorData", resource_id=data_id)
        
        # # If sensor_id is being updated, check if the new sensor exists
        # if sensor_data.sensor_id is not None and sensor_data.sensor_id != existing_data.sensor_id:
        #     from app.services import SensorService
        #     sensor_service = SensorService()
        #     sensor = await sensor_service.get_sensor(sensor_data.sensor_id)
        #     if not sensor:
        #         raise NotFoundException(resource_name="Sensor", resource_id=sensor_data.sensor_id)
        
        updated_data = await service.update_sensor_data(data_id, sensor_data)
        return updated_data
    except HTTPException:  
       raise 
    except NotFoundException as e:
        logger.warning(f"Resource not found for sensor data update: {str(e)}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in update_sensor_data: {str(e)}")
        raise
    except ValueError as e:
        logger.error(f"Validation error while updating sensor data {data_id}: {str(e)}")
        raise ValidationException(detail=str(e))
    except ConflictException as e:
        logger.warning(f"Conflict while updating sensor data {data_id}: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while updating sensor data {data_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while updating sensor data {data_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to update sensor data with id {data_id}")


@router.put("/{data_id}/validate", response_model=SensorData)
async def validate_sensor_data(data_id: int):
    """Validate sensor data"""
    try:
        if data_id <= 0:
            raise BadRequestException(detail="Data ID must be positive")
        
        service = SensorDataService()
        
        # Check if sensor data exists
        existing_data = await service.get_sensor_data(data_id)
        if not existing_data:
            raise NotFoundException(resource_name="SensorData", resource_id=data_id)
        
        # Check if data is already validated
        if existing_data.status == DataStatus.VALIDATED:
            raise ConflictException(detail=f"Sensor data {data_id} is already validated")
        
        # Check if data is archived
        if existing_data.status == DataStatus.ARCHIVED:
            raise ConflictException(detail=f"Cannot validate archived sensor data {data_id}")
        
        validated_data = await service.validate_sensor_data(data_id)
        return validated_data
    except HTTPException:  
       raise 
    except NotFoundException as e:
        logger.warning(f"Sensor data not found for validation: {data_id}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in validate_sensor_data: {str(e)}")
        raise
    except ConflictException as e:
        logger.warning(f"Conflict while validating sensor data {data_id}: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while validating sensor data {data_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while validating sensor data {data_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to validate sensor data with id {data_id}")


@router.put("/{data_id}/archive", response_model=SensorData)
async def archive_sensor_data(data_id: int):
    """Archive sensor data"""
    try:
        if data_id <= 0:
            raise BadRequestException(detail="Data ID must be positive")
        
        service = SensorDataService()
        
        # Check if sensor data exists
        existing_data = await service.get_sensor_data(data_id)
        if not existing_data:
            raise NotFoundException(resource_name="SensorData", resource_id=data_id)
        
        # Check if data is already archived
        if existing_data.status == DataStatus.ARCHIVED:
            raise ConflictException(detail=f"Sensor data {data_id} is already archived")
        
        archived_data = await service.archive_sensor_data(data_id)
        return archived_data
    except HTTPException:  
       raise 
    except NotFoundException as e:
        logger.warning(f"Sensor data not found for archiving: {data_id}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in archive_sensor_data: {str(e)}")
        raise
    except ConflictException as e:
        logger.warning(f"Conflict while archiving sensor data {data_id}: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while archiving sensor data {data_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while archiving sensor data {data_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to archive sensor data with id {data_id}")


@router.delete("/{data_id}")
async def delete_sensor_data(data_id: int):
    """Delete sensor data"""
    try:
        if data_id <= 0:
            raise BadRequestException(detail="Data ID must be positive")
        
        service = SensorDataService()
        
        # Check if sensor data exists
        existing_data = await service.get_sensor_data(data_id)
        if not existing_data:
            raise NotFoundException(resource_name="SensorData", resource_id=data_id)
        
        result = await service.delete_sensor_data(data_id)
        
        return {
            "message": f"Sensor data with id {data_id} deleted successfully",
            "deleted_id": data_id
        }
    except HTTPException:  
       raise 
    except NotFoundException as e:
        logger.warning(f"Sensor data not found for deletion: {data_id}")
        raise
    except BadRequestException as e:
        logger.warning(f"Bad request in delete_sensor_data: {str(e)}")
        raise
    except DatabaseException as e:
        logger.error(f"Database error while deleting sensor data {data_id}: {str(e)}")
        raise
    except Exception as e:
        logger.critical(f"Unexpected error while deleting sensor data {data_id}: {str(e)}")
        raise InternalServerException(detail=f"Failed to delete sensor data with id {data_id}")