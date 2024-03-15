from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator

from .constants import ErrorCode


class DeviceBase(BaseModel):
    name: str = Field(..., description="Unique name for the device")
    device_type: str = Field(..., description="Type of the device")
    host: str = Field(..., description="Host address of the device")
    port: int = Field(..., description="Network port of the device")
    protocol: str = Field(..., description="Network protocol used by the device")
    zone_name: Optional[str] = Field(None, description="Name of the associated zone")
    zone_id: Optional[UUID4] = Field(None, description="UUID of the associated zone")
    credential_id: Optional[UUID4] = Field(None, description="UUID of the associated credential")


class DeviceCreate(DeviceBase):
    @model_validator(mode="after")
    def check_vpc_id_or_name(self):
        if self.zone_id and self.zone_name:
            raise ValueError(ErrorCode.DEVICE_ZONE_ID_OR_NAME_ERROR)
        return self


class DeviceUpdate(DeviceCreate):
    pass


class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the device")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
