from typing import Optional, List, Dict
from app.repositories.base import BaseRepository
from app.models import SensorCreate, SensorUpdate


class SensorRepository(BaseRepository):
    """Repository for Sensor entity operations"""
    
    async def create(self, sensor: SensorCreate) -> Dict:
        """Create a new sensor"""
        query = """
            INSERT INTO sensors (name, sensor_type, unit_id, status, description)
            VALUES ($1, $2, $3, $4, $5)
            RETURNING id, name, sensor_type, unit_id, status, description, created_at
        """
        record = await self.fetch_one(
            query,
            sensor.name,
            sensor.sensor_type.value,
            sensor.unit_id,
            sensor.status.value,
            sensor.description
        )
        return self.record_to_dict(record)
    
    async def get_by_id(self, sensor_id: int) -> Optional[Dict]:
        """Get sensor by ID"""
        query = """
            SELECT id, name, sensor_type, unit_id, status, description, created_at
            FROM sensors
            WHERE id = $1
        """
        record = await self.fetch_one(query, sensor_id)
        return self.record_to_dict(record)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all sensors with pagination"""
        query = """
            SELECT id, name, sensor_type, unit_id, status, description, created_at
            FROM sensors
            ORDER BY created_at DESC
            LIMIT $1 OFFSET $2
        """
        records = await self.fetch_all(query, limit, skip)
        return self.records_to_list(records)
    
    async def get_by_unit_id(self, unit_id: int, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all sensors for a specific unit"""
        query = """
            SELECT id, name, sensor_type, unit_id, status, description, created_at
            FROM sensors
            WHERE unit_id = $1
            ORDER BY created_at DESC
            LIMIT $2 OFFSET $3
        """
        records = await self.fetch_all(query, unit_id, limit, skip)
        return self.records_to_list(records)
    
    async def update(self, sensor_id: int, sensor: SensorUpdate) -> Optional[Dict]:
        """Update a sensor"""
        update_fields = []
        values = []
        param_count = 1
        
        if sensor.name is not None:
            update_fields.append(f"name = ${param_count}")
            values.append(sensor.name)
            param_count += 1
        
        if sensor.sensor_type is not None:
            update_fields.append(f"sensor_type = ${param_count}")
            values.append(sensor.sensor_type.value)
            param_count += 1
        
        if sensor.status is not None:
            update_fields.append(f"status = ${param_count}")
            values.append(sensor.status.value)
            param_count += 1
        
        if sensor.description is not None:
            update_fields.append(f"description = ${param_count}")
            values.append(sensor.description)
            param_count += 1
        
        if not update_fields:
            return await self.get_by_id(sensor_id)
        
        values.append(sensor_id)
        query = f"""
            UPDATE sensors
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, name, sensor_type, unit_id, status, description, created_at
        """
        
        record = await self.fetch_one(query, *values)
        return self.record_to_dict(record)
    
    async def delete(self, sensor_id: int) -> bool:
        """Delete a sensor"""
        query = "DELETE FROM sensors WHERE id = $1"
        result = await self.execute(query, sensor_id)
        return result == "DELETE 1"
    
    async def exists_for_unit(self, unit_id: int) -> bool:
        """Check if unit has any sensors"""
        query = "SELECT EXISTS(SELECT 1 FROM sensors WHERE unit_id = $1)"
        return await self.fetch_val(query, unit_id)
