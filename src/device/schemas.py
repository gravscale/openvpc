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
    credential_id: Optional[UUID4] = Field(None, description="UUID of the associated credential")


class DeviceCreate(DeviceBase):
    zone_id: Optional[UUID4] = Field(None, description="UUID of the associated zone")
    zone_name: Optional[str] = Field(None, description="Name of the associated zone")

    @model_validator(mode="after")
    def check_zone_id_and_name(self):
        if self.zone_id and self.zone_name:
            raise ValueError(ErrorCode.ZONE_ID_AND_NAME_PROVIDED)

        if not self.zone_id and not self.zone_name:
            raise ValueError(ErrorCode.ZONE_ID_OR_NAME_REQUIRED)

        return self


class DeviceUpdate(DeviceCreate):
    pass


class DeviceResponse(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the device")
    zone_id: UUID4 = Field(..., description="UUID of the associated zone")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
