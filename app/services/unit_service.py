from typing import List, Optional
from app.repositories import UnitRepository
from app.models import Unit, UnitCreate, UnitUpdate, UnitStatistics
from app.exceptions import NotFoundException, BadRequestException


class UnitService:
    """Service layer for Unit business logic"""
    
    def __init__(self):
        self.repository = UnitRepository()
    
    async def create_unit(self, unit: UnitCreate) -> Unit:
        """Create a new unit"""
        unit_data = await self.repository.create(unit)
        return Unit(**unit_data)
    
    async def get_unit(self, unit_id: int) -> Unit:
        """Get unit by ID"""
        unit_data = await self.repository.get_by_id(unit_id)
        if not unit_data:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)  
        return Unit(**unit_data)
    
    async def get_all_units(self, skip: int = 0, limit: int = 100) -> List[Unit]:
        """Get all units with pagination"""
        if limit > 100:
            raise BadRequestException(detail="Limit cannot exceed 100")  
        units_data = await self.repository.get_all(skip, limit)
        return [Unit(**unit) for unit in units_data]
    
    async def update_unit(self, unit_id: int, unit: UnitUpdate) -> Unit:
        """Update a unit"""
        existing_unit = await self.repository.get_by_id(unit_id)
        if not existing_unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)  
        
        unit_data = await self.repository.update(unit_id, unit)
        return Unit(**unit_data)
    
    async def delete_unit(self, unit_id: int) -> dict:
        """Delete a unit"""
        existing_unit = await self.repository.get_by_id(unit_id)
        if not existing_unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)  
        
        deleted = await self.repository.delete(unit_id)
        if not deleted:
            raise BadRequestException(detail="Failed to delete unit")  
        
        return {"message": "Unit deleted successfully"}
    
    async def get_unit_statistics(self, unit_id: int) -> UnitStatistics:
        """Get statistics for a unit"""
        existing_unit = await self.repository.get_by_id(unit_id)
        if not existing_unit:
            raise NotFoundException(resource_name="Unit", resource_id=unit_id)  
        
        stats_data = await self.repository.get_statistics(unit_id)
        if not stats_data:
            raise NotFoundException(resource_name="Statistics", resource_id=unit_id)  
        
        return UnitStatistics(**stats_data)