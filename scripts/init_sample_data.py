import asyncio
import asyncpg
import os
from pathlib import Path

# Get settings from environment
DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", 5432))
DATABASE_USER = os.getenv("DATABASE_USER", "iot_user")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "1245")
DATABASE_NAME = os.getenv("DATABASE_NAME", "iot_sensors")


async def init_data():
    """Initialize sample data"""
    conn = await asyncpg.connect(
        host=DATABASE_HOST,
        port=DATABASE_PORT,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        database=DATABASE_NAME
    )
    
    try:
        # Check if data already exists
        count = await conn.fetchval("SELECT COUNT(*) FROM units")
        if count > 0:
            print("✅ Sample data already exists")
            return
        
        # Insert sample units
        unit1_id = await conn.fetchval("""
            INSERT INTO units (name, location, description)
            VALUES ('Factory A', 'Building 1, Floor 2', 'Main production unit')
            RETURNING id
        """)
        
        unit2_id = await conn.fetchval("""
            INSERT INTO units (name, location, description)
            VALUES ('Warehouse B', 'Building 3', 'Storage facility')
            RETURNING id
        """)
        
        # Insert sample sensors
        sensor1_id = await conn.fetchval("""
            INSERT INTO sensors (name, sensor_type, unit_id, status, description)
            VALUES ('Temperature Sensor 1', 'temperature', $1, 'active', 'Monitors room temperature')
            RETURNING id
        """, unit1_id)
        
        sensor2_id = await conn.fetchval("""
            INSERT INTO sensors (name, sensor_type, unit_id, status, description)
            VALUES ('Humidity Sensor 1', 'humidity', $1, 'active', 'Monitors air humidity')
            RETURNING id
        """, unit1_id)
        
        await conn.fetchval("""
            INSERT INTO sensors (name, sensor_type, unit_id, status, description)
            VALUES ('Pressure Sensor 1', 'pressure', $1, 'inactive', 'Monitors air pressure')
            RETURNING id
        """, unit2_id)
        
        # Insert sample sensor data
        await conn.execute("""
            INSERT INTO sensor_data (sensor_id, value, unit, status)
            VALUES 
                ($1, 23.5, 'celsius', 'validated'),
                ($1, 24.1, 'celsius', 'validated'),
                ($2, 65.0, 'percent', 'pending')
        """, sensor1_id, sensor2_id)
        
        print("✅ Sample data initialized successfully!")
        
    finally:
        await conn.close()


if __name__ == "__main__":
    asyncio.run(init_data())