# schemas.py
from pydantic_core.core_schema import FieldValidationInfo
from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from uuid import UUID
from datetime import datetime

class CredentialBase(BaseModel):
    name: str = Field(..., description="Unique name for the credential")
    user: str = Field(..., description="Username associated with the credential")
    private_key: Optional[str] = Field(None, description="Private key if applicable")
    password: Optional[str] = Field(None, description="Password if applicable")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
    is_active: bool = Field(True, description="Active status of the credential")

    @field_validator('private_key', 'password') 
    def check_either_private_key_or_password(cls, v, info: FieldValidationInfo): 
        if 'private_key' in info.data and 'password' in info.data: 
            raise ValueError("Provide either private_key or password, not both")
        return v


class CredentialCreate(CredentialBase):
    pass

class CredentialUpdate(CredentialBase):
    pass

class CredentialRead(CredentialBase):
    id: str = Field(..., description="Unique identifier for the credential")

class DeviceBase(BaseModel):
    name: str = Field(..., description="Unique name for the device")
    device_type: str = Field(..., description="Type of the device")
    host: str = Field(..., description="Host address of the device")
    port: int = Field(..., description="Network port of the device")
    protocol: str = Field(..., description="Network protocol used by the device")
    zone_uuid: Optional[str] = Field(None, description="UUID of the associated zone")
    zone_name: Optional[str] = Field(None, description="Name of the associated zone")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
    is_active: bool = Field(True, description="Active status of the device")

    @field_validator('zone_uuid', 'zone_name')  
    def check_either_zone_uuid_or_name(cls, v, info: FieldValidationInfo):  
        if 'zone_uuid' in info.data and 'zone_name' in info.data:  
            raise ValueError("Provide either zone_uuid or zone_name, not both")
        return v

    @field_validator('zone_uuid', 'zone_name')  
    def validate_uuid(cls, v, info: FieldValidationInfo):  
        if info.field_name == 'zone_uuid' and v:  
            try:
                UUID(v)
            except ValueError:
                raise ValueError("Invalid UUID format")
        return v

    credential_id: Optional[str] = Field(None, description="UUID of the associated credential")

    @field_validator('credential_id')
    def validate_credential_uuid(cls, v):
        if v:
            try:
                UUID(v)
            except ValueError:
                raise ValueError("Invalid UUID format for credential")
        return v

class DeviceCreate(DeviceBase):
    pass

class DeviceUpdate(DeviceBase):
    pass

class DeviceRead(DeviceBase):
    id: str = Field(..., description="Unique identifier for the device")
