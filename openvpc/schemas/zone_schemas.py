from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class ZoneCreate(BaseModel):
    name: str = Field(..., description="Unique name for the zone")


class ZoneRead(BaseModel):
    id: str = Field(..., description="Unique identifier for the zone")
    name: str = Field(..., description="Unique name for the zone")
    is_active: bool = Field(True, description="Active status of the device")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")

    class Config:
        from_attributes = True
