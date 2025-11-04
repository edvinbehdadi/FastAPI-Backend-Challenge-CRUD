"""
API Examples and Response Schemas
"""

# ============= SENSOR EXAMPLES =============

SENSOR_EXAMPLE = {
    "name": "Temperature Sensor 1",
    "sensor_type": "temperature",
    "unit_id": 1,
    "status": "active",
    "description": "Monitors room temperature in production area"
}

SENSOR_RESPONSE_EXAMPLE = {
    "id": 1,
    "name": "Temperature Sensor 1",
    "sensor_type": "temperature",
    "unit_id": 1,
    "status": "active",
    "description": "Monitors room temperature",
    "created_at": "2025-01-15T10:30:00Z"
}

SENSOR_CREATE_DESCRIPTION = """
Create a new IoT sensor for a specific unit.

**Sensor Types:**
- `temperature`: Temperature sensors (celsius/fahrenheit)
- `humidity`: Humidity sensors (percentage)
- `pressure`: Pressure sensors (pascal/bar)
- `motion`: Motion detection sensors
- `light`: Light intensity sensors (lux)
- `sound`: Sound level sensors (decibels)

**Sensor Status:**
- `active`: Sensor is operational and collecting data
- `inactive`: Sensor is not currently collecting data
- `maintenance`: Sensor is under maintenance
"""

SENSOR_RESPONSES = {
    201: {
        "description": "Sensor created successfully",
        "content": {
            "application/json": {
                "example": SENSOR_RESPONSE_EXAMPLE
            }
        }
    },
    404: {"description": "Unit not found"},
    422: {"description": "Validation error"}
}

# ============= UNIT EXAMPLES =============

UNIT_EXAMPLE = {
    "name": "Factory A",
    "location": "Building 1, Floor 2",
    "description": "Main production unit"
}

UNIT_RESPONSE_EXAMPLE = {
    "id": 1,
    "name": "Factory A",
    "location": "Building 1, Floor 2",
    "description": "Main production unit",
    "created_at": "2025-01-15T10:30:00Z"
}

UNIT_CREATE_DESCRIPTION = """
Create a new unit (facility/location) where IoT sensors will be deployed.

Units represent physical locations such as:
- Factories
- Warehouses
- Office buildings
- Production lines
"""

UNIT_RESPONSES = {
    201: {
        "description": "Unit created successfully",
        "content": {
            "application/json": {
                "example": UNIT_RESPONSE_EXAMPLE
            }
        }
    },
    422: {"description": "Validation error"}
}

# ============= SENSOR DATA EXAMPLES =============

SENSOR_DATA_EXAMPLE = {
    "sensor_id": 1,
    "value": 23.5,
    "unit": "celsius",
    "status": "pending"
}

SENSOR_DATA_RESPONSE_EXAMPLE = {
    "id": 1,
    "sensor_id": 1,
    "value": 23.5,
    "unit": "celsius",
    "status": "pending",
    "timestamp": "2025-01-15T10:30:00Z"
}

SENSOR_DATA_CREATE_DESCRIPTION = """
Record a new data point from an IoT sensor.

**Data Status:**
- `pending`: Awaiting validation
- `validated`: Data has been verified and approved
- `archived`: Old data moved to archive
- `invalid`: Data marked as invalid/erroneous

**Common Units:**
- Temperature: celsius, fahrenheit, kelvin
- Humidity: percent, ratio
- Pressure: pascal, bar, psi
- Motion: boolean, count
- Light: lux, lumens
- Sound: decibels
"""

SENSOR_DATA_RESPONSES = {
    201: {
        "description": "Sensor data created successfully",
        "content": {
            "application/json": {
                "example": SENSOR_DATA_RESPONSE_EXAMPLE
            }
        }
    },
    404: {"description": "Sensor not found"},
    422: {"description": "Validation error"}
}