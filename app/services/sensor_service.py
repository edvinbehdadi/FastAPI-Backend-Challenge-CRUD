from typing import List, Optional
from fastapi import HTTPException, status
from app.repositories import SensorRepository, UnitRepository
from app.models import Sensor, SensorCreate, SensorUpdate


class SensorService:
    """Service layer for Sensor business logic"""
    
    def __init__(self):
        self.repository = SensorRepository()
        self.unit_repository = UnitRepository()
    
    async def create_sensor(self, sensor: SensorCreate) -> Sensor:
        """Create a new sensor"""
        # Verify that unit exists
        unit = await self.unit_repository.get_by_id(sensor.unit_id)
        if not unit:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Unit with id {sensor.unit_id} not found"
            )
        
        sensor_data = await self.repository.create(sensor)
        return Sensor(**sensor_data)
    
    async def get_sensor(self, sensor_id: int) -> Sensor:
        """Get sensor by ID"""
        sensor_data = await self.repository.get_by_id(sensor_id)
        if not sensor_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor with id {sensor_id} not found"
            )
        return Sensor(**sensor_data)
    
    async def get_all_sensors(self, skip: int = 0, limit: int = 100, unit_id: Optional[int] = None) -> List[Sensor]:
        """Get all sensors with optional filtering by unit_id"""
        if limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Limit cannot exceed 100"
            )
        
        if unit_id is not None:
            sensors_data = await self.repository.get_by_unit_id(unit_id, skip, limit)
        else:
            sensors_data = await self.repository.get_all(skip, limit)
        
        return [Sensor(**sensor) for sensor in sensors_data]
    
    async def update_sensor(self, sensor_id: int, sensor: SensorUpdate) -> Sensor:
        """Update a sensor"""
        # Check if sensor exists
        existing_sensor = await self.repository.get_by_id(sensor_id)
        if not existing_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor with id {sensor_id} not found"
            )
        
        sensor_data = await self.repository.update(sensor_id, sensor)
        return Sensor(**sensor_data)
    
    async def delete_sensor(self, sensor_id: int) -> dict:
        """Delete a sensor"""
        # Check if sensor exists
        existing_sensor = await self.repository.get_by_id(sensor_id)
        if not existing_sensor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Sensor with id {sensor_id} not found"
            )
        
        deleted = await self.repository.delete(sensor_id)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to delete sensor"
            )
        
        return {"message": "Sensor deleted successfully"}
