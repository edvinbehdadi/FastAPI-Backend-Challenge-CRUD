from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories import SensorDataRepository, SensorRepository
from app.models import SensorData, SensorDataCreate, SensorDataUpdate, DataStatus, SensorDataWithDetails
from app.exceptions import NotFoundException, BadRequestException


class SensorDataService:
    """Service layer for SensorData business logic"""
    
    def __init__(self):
        self.repository = SensorDataRepository()
        self.sensor_repository = SensorRepository()
    
    async def create_sensor_data(self, sensor_data: SensorDataCreate) -> SensorData:
        """Create a new sensor data entry"""
        # Verify that sensor exists
        sensor = await self.sensor_repository.get_by_id(sensor_data.sensor_id)
        if not sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor with id {sensor_data.sensor_id} not found"
            )
        
        data = await self.repository.create(sensor_data)
        return SensorData(**data)
    
    async def get_sensor_data(self, data_id: int) -> SensorData:
        """Get sensor data by ID"""
        data = await self.repository.get_by_id(data_id)
        if not data:
            raise NotFoundException(resource_name="Sensor data", resource_id=data_id)
        return SensorData(**data)
    
    async def get_all_sensor_data(
        self,
        skip: int = 0,
        limit: int = 100,
        sensor_id: Optional[int] = None,
        status_filter: Optional[DataStatus] = None,
        with_details: bool = False
    ) -> List[SensorData] | List[SensorDataWithDetails]:
        """Get all sensor data with optional filtering"""
        if limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit cannot exceed 100"
            )
        
        if with_details:
            data_list = await self.repository.get_with_details(skip, limit)
            return [SensorDataWithDetails(**data) for data in data_list]
        
        if sensor_id is not None:
            data_list = await self.repository.get_by_sensor_id(sensor_id, skip, limit)
        elif status_filter is not None:
            data_list = await self.repository.get_by_status(status_filter, skip, limit)
        else:
            data_list = await self.repository.get_all(skip, limit)
        
        return [SensorData(**data) for data in data_list]
    
    async def update_sensor_data(self, data_id: int, sensor_data: SensorDataUpdate) -> SensorData:
        """Update sensor data"""
        # Check if data exists
        existing_data = await self.repository.get_by_id(data_id)
        if not existing_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor data with id {data_id} not found"
            )
        
        data = await self.repository.update(data_id, sensor_data)
        return SensorData(**data)
    
    async def validate_sensor_data(self, data_id: int) -> SensorData:
        """Validate sensor data"""
        # Check if data exists
        existing_data = await self.repository.get_by_id(data_id)
        if not existing_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor data with id {data_id} not found"
            )
        
        data = await self.repository.validate(data_id)
        return SensorData(**data)
    
    async def archive_sensor_data(self, data_id: int) -> SensorData:
        """Archive sensor data"""
        # Check if data exists
        existing_data = await self.repository.get_by_id(data_id)
        if not existing_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor data with id {data_id} not found"
            )
        
        data = await self.repository.archive(data_id)
        return SensorData(**data)
    
    async def delete_sensor_data(self, data_id: int) -> dict:
        """Delete sensor data"""
        # Check if data exists
        existing_data = await self.repository.get_by_id(data_id)
        if not existing_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor data with id {data_id} not found"
            )
        
        deleted = await self.repository.delete(data_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete sensor data"
            )
        
        return {"message": "Sensor data deleted successfully"}
