from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class UnitBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    location: str = Field(..., min_length=1, max_length=500)
    description: Optional[str] = None


class UnitCreate(UnitBase):
    pass


class UnitUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[str] = Field(None, min_length=1, max_length=500)
    description: Optional[str] = None


class Unit(UnitBase):
    id: int
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UnitStatistics(BaseModel):
    unit_id: int
    unit_name: str
    total_sensors: int
    active_sensors: int
    inactive_sensors: int
    total_data_points: int
    latest_data_timestamp: Optional[datetime] = None