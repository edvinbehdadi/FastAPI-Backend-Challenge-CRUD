from typing import Optional, List, Dict
from app.repositories.base import BaseRepository
from app.models import UnitCreate, UnitUpdate


class UnitRepository(BaseRepository):
    """Repository for Unit entity operations"""
    
    async def create(self, unit: UnitCreate) -> Dict:
        """Create a new unit"""
        query = """
            INSERT INTO units (name, location, description)
            VALUES ($1, $2, $3)
            RETURNING id, name, location, description, created_at
        """
        record = await self.fetch_one(
            query,
            unit.name,
            unit.location,
            unit.description
        )
        return self.record_to_dict(record)
    
    async def get_by_id(self, unit_id: int) -> Optional[Dict]:
        """Get unit by ID"""
        query = """
            SELECT id, name, location, description, created_at
            FROM units
            WHERE id = $1
        """
        record = await self.fetch_one(query, unit_id)
        return self.record_to_dict(record)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all units with pagination"""
        query = """
            SELECT id, name, location, description, created_at
            FROM units
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
        """
        records = await self.fetch_all(query, limit, skip)
        return self.records_to_list(records)
    
    async def update(self, unit_id: int, unit: UnitUpdate) -> Optional[Dict]:
        """Update a unit"""
        # Build dynamic update query based on provided fields
        update_fields = []
        values = []
        param_count = 1
        
        if unit.name is not None:
            update_fields.append(f"name = ${param_count}")
            values.append(unit.name)
            param_count += 1
        
        if unit.location is not None:
            update_fields.append(f"location = ${param_count}")
            values.append(unit.location)
            param_count += 1
        
        if unit.description is not None:
            update_fields.append(f"description = ${param_count}")
            values.append(unit.description)
            param_count += 1
        
        if not update_fields:
            return await self.get_by_id(unit_id)
        
        values.append(unit_id)
        query = f"""
            UPDATE units
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, name, location, description, created_at
        """
        
        record = await self.fetch_one(query, *values)
        return self.record_to_dict(record)
    
    async def delete(self, unit_id: int) -> bool:
        """Delete a unit"""
        query = "DELETE FROM units WHERE id = $1"
        result = await self.execute(query, unit_id)
        return result == "DELETE 1"
    
    async def get_statistics(self, unit_id: int) -> Optional[Dict]:
        """Get statistics for a specific unit"""
        query = """
            SELECT 
                u.id as unit_id,
                u.name as unit_name,
                COUNT(DISTINCT s.id) as total_sensors,
                COUNT(DISTINCT CASE WHEN s.status = 'active' THEN s.id END) as active_sensors,
                COUNT(DISTINCT CASE WHEN s.status = 'inactive' THEN s.id END) as inactive_sensors,
                COUNT(sd.id) as total_data_points,
                MAX(sd.timestamp) as latest_data_timestamp
            FROM units u
            LEFT JOIN sensors s ON s.unit_id = u.id
            LEFT JOIN sensor_data sd ON sd.sensor_id = s.id
            WHERE u.id = $1
            GROUP BY u.id, u.name
        """
        record = await self.fetch_one(query, unit_id)
        return self.record_to_dict(record)
