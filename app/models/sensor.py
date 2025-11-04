from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class SensorType(str, Enum):
    """Available sensor types"""
    temperature = "temperature"
    humidity = "humidity"
    pressure = "pressure"
    motion = "motion"
    light = "light"
    sound = "sound"



class SensorStatus(str, Enum):
    """Sensor status options"""
    active = "active"
    inactive = "inactive"
    maintenance = "maintenance"

class SensorBase(BaseModel):
    """Base sensor model"""
    name: str = Field(..., description="Sensor name", example="Temperature Sensor 1")
    sensor_type: SensorType = Field(..., description="Type of sensor", example="temperature")
    unit_id: int = Field(..., description="ID of the unit this sensor belongs to", example=1)
    status: SensorStatus = Field(
        default=SensorStatus.active,
        description="Current status of the sensor",
        example="active"
    )
    description: Optional[str] = Field(
        None,
        description="Additional description about the sensor",
        example="Monitors room temperature in production area"
    )


class SensorCreate(SensorBase):
    pass


class SensorUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sensor_type: Optional[SensorType] = None
    status: Optional[SensorStatus] = None
    description: Optional[str] = None


class Sensor(SensorBase):
    """Complete sensor model with metadata"""
    id: int = Field(..., description="Unique sensor ID")
    created_at: datetime = Field(..., description="Timestamp when sensor was created")

    class Config:
        from_attributes = True