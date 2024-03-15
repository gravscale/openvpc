from datetime import datetime

from pydantic import UUID4, BaseModel, ConfigDict, Field


class VpcCreate(BaseModel):
    name: str = Field(..., description="Unique name for the vpc")
    device_name_primary: str = Field(..., description="Primary device name")
    device_name_secondary: str = Field(..., description="Secondary device name")


class VpcResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the vpc")
    name: str = Field(..., description="Unique name for the vpc")
    device_name_primary: str = Field(..., description="Primary device name")
    device_name_secondary: str = Field(..., description="Secondary device name")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
