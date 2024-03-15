from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field


class ZoneCreate(BaseModel):
    name: str = Field(..., description="Unique name for the zone")


class ZoneResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the zone")
    name: str = Field(..., description="Unique name for the zone")
    is_active: bool = Field(True, description="Active status of the zone")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
