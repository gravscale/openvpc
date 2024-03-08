from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class DeviceBase(BaseModel):
    name: str = Field(..., description="Unique name for the device")
    device_type: str = Field(..., description="Type of the device")
    host: str = Field(..., description="Host address of the device")
    port: int = Field(..., description="Network port of the device")
    protocol: str = Field(..., description="Network protocol used by the device")
    zone_name: Optional[str] = Field(None, description="Name of the associated zone")
    zone_id: Optional[UUID] = Field(None, description="UUID of the associated zone")
    credential_id: Optional[UUID] = Field(None, description="UUID of the associated credential")

    @field_validator("zone_id", "zone_name")
    def check_either_zone_uuid_or_name(cls, v, info: ValidationInfo):
        if "zone_id" in info.data and "zone_name" in info.data:
            raise ValueError("Provide either zone_id or zone_name, not both")
        return v

    # @field_validator("zone_id", "zone_name")
    # def validate_zone_uuid(cls, v, info: ValidationInfo):
    #     if info.field_name == "zone_id" and v:
    #         try:
    #             UUID(v)
    #         except ValueError:
    #             raise ValueError("Invalid UUID format")
    #     return v

    # @field_validator("credential_id")
    # def validate_credential_uuid(cls, v):
    #     if v:
    #         try:
    #             UUID(v)
    #         except ValueError:
    #             raise ValueError("Invalid UUID format for credential")
    #     return v


class DeviceCreate(DeviceBase):
    pass


class DeviceUpdate(DeviceBase):
    pass


class DeviceRead(DeviceBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID = Field(..., description="Unique identifier for the device")
    is_active: bool = Field(True, description="Active status of the device")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
