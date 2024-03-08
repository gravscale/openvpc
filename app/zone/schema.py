from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ZoneCreate(BaseModel):
    name: str = Field(..., description="Unique name for the zone")


class ZoneRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique identifier for the zone")
    name: str = Field(..., description="Unique name for the zone")
    is_active: bool = Field(True, description="Active status of the zone")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
