from typing import Optional, List, Dict
from app.repositories.base import BaseRepository
from app.models import SensorDataCreate, SensorDataUpdate, DataStatus


class SensorDataRepository(BaseRepository):
    """Repository for SensorData entity operations"""
    
    async def create(self, sensor_data: SensorDataCreate) -> Dict:
        """Create a new sensor data entry"""
        query = """
            INSERT INTO sensor_data (sensor_id, value, unit, status)
            VALUES ($1, $2, $3, $4)
            RETURNING id, sensor_id, value, unit, status, timestamp
        """
        record = await self.fetch_one(
            query,
            sensor_data.sensor_id,
            sensor_data.value,
            sensor_data.unit,
            sensor_data.status.value
        )
        return self.record_to_dict(record)
    
    async def get_by_id(self, data_id: int) -> Optional[Dict]:
        """Get sensor data by ID"""
        query = """
            SELECT id, sensor_id, value, unit, status, timestamp
            FROM sensor_data
            WHERE id = $1
        """
        record = await self.fetch_one(query, data_id)
        return self.record_to_dict(record)
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all sensor data with pagination"""
        query = """
            SELECT id, sensor_id, value, unit, status, timestamp
            FROM sensor_data
            ORDER BY timestamp DESC
            LIMIT $1 OFFSET $2
        """
        records = await self.fetch_all(query, limit, skip)
        return self.records_to_list(records)
    
    async def get_by_sensor_id(self, sensor_id: int, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all data for a specific sensor"""
        query = """
            SELECT id, sensor_id, value, unit, status, timestamp
            FROM sensor_data
            WHERE sensor_id = $1
            ORDER BY timestamp DESC
            LIMIT $2 OFFSET $3
        """
        records = await self.fetch_all(query, sensor_id, limit, skip)
        return self.records_to_list(records)
    
    async def get_by_status(self, status: DataStatus, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get all data by status"""
        query = """
            SELECT id, sensor_id, value, unit, status, timestamp
            FROM sensor_data
            WHERE status = $1
            ORDER BY timestamp DESC
            LIMIT $2 OFFSET $3
        """
        records = await self.fetch_all(query, status.value, limit, skip)
        return self.records_to_list(records)
    
    async def get_with_details(self, skip: int = 0, limit: int = 100) -> List[Dict]:
        """Get sensor data with sensor and unit details"""
        query = """
            SELECT 
                sd.id,
                sd.sensor_id,
                sd.value,
                sd.unit,
                sd.status,
                sd.timestamp,
                s.name as sensor_name,
                s.sensor_type,
                u.name as unit_name
            FROM sensor_data sd
            JOIN sensors s ON sd.sensor_id = s.id
            JOIN units u ON s.unit_id = u.id
            ORDER BY sd.timestamp DESC
            LIMIT $1 OFFSET $2
        """
        records = await self.fetch_all(query, limit, skip)
        return self.records_to_list(records)
    
    async def update(self, data_id: int, sensor_data: SensorDataUpdate) -> Optional[Dict]:
        """Update sensor data"""
        update_fields = []
        values = []
        param_count = 1
        
        if sensor_data.value is not None:
            update_fields.append(f"value = ${param_count}")
            values.append(sensor_data.value)
            param_count += 1
        
        if sensor_data.unit is not None:
            update_fields.append(f"unit = ${param_count}")
            values.append(sensor_data.unit)
            param_count += 1
        
        if sensor_data.status is not None:
            update_fields.append(f"status = ${param_count}")
            values.append(sensor_data.status.value)
            param_count += 1
        
        if not update_fields:
            return await self.get_by_id(data_id)
        
        values.append(data_id)
        query = f"""
            UPDATE sensor_data
            SET {', '.join(update_fields)}
            WHERE id = ${param_count}
            RETURNING id, sensor_id, value, unit, status, timestamp
        """
        
        record = await self.fetch_one(query, *values)
        return self.record_to_dict(record)
    
    async def validate(self, data_id: int) -> Optional[Dict]:
        """Mark sensor data as validated"""
        query = """
            UPDATE sensor_data
            SET status = $1
            WHERE id = $2
            RETURNING id, sensor_id, value, unit, status, timestamp
        """
        record = await self.fetch_one(query, DataStatus.VALIDATED.value, data_id)
        return self.record_to_dict(record)
    
    async def archive(self, data_id: int) -> Optional[Dict]:
        """Mark sensor data as archived"""
        query = """
            UPDATE sensor_data
            SET status = $1
            WHERE id = $2
            RETURNING id, sensor_id, value, unit, status, timestamp
        """
        record = await self.fetch_one(query, DataStatus.ARCHIVED.value, data_id)
        return self.record_to_dict(record)
    
    async def delete(self, data_id: int) -> bool:
        """Delete sensor data"""
        query = "DELETE FROM sensor_data WHERE id = $1"
        result = await self.execute(query, data_id)
        return result == "DELETE 1"
