from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum


class DataStatus(str, Enum):
    PENDING = "pending"
    VALIDATED = "validated"
    ARCHIVED = "archived"
    INVALID = "invalid"


class SensorDataBase(BaseModel):
    sensor_id: int
    value: float
    unit: Optional[str] = None
    status: DataStatus = DataStatus.PENDING


class SensorDataCreate(SensorDataBase):
    pass


class SensorDataUpdate(BaseModel):
    value: Optional[float] = None
    unit: Optional[str] = None
    status: Optional[DataStatus] = None
    


class SensorData(SensorDataBase):
    id: int
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SensorDataWithDetails(SensorData):
    sensor_name: str
    sensor_type: str
    unit_name: str