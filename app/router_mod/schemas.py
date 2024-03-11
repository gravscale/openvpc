from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, Field, field_validator
from pydantic_core.core_schema import ValidationInfo


class RouterBase(BaseModel):
    name: str = Field(..., description="Unique name for the router")
    vpc_uuid: Optional[str] = Field(None, description="UUID of the associated VPC")
    vpc_name: Optional[str] = Field(None, description="Name of the associated VPC")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    deleted_at: Optional[datetime] = Field(None, description="Deletion timestamp")
    is_active: bool = Field(True, description="Active status of the router")

    @field_validator("vpc_uuid", "vpc_name")
    def check_vpc_uuid_or_name(cls, v, info: ValidationInfo):
        if ("vpc_uuid" in info.data and "vpc_name" in info.data) or (
            "vpc_name" in info.data and "vpc_uuid" in info.data
        ):
            raise ValueError("Provide either vpc_uuid or vpc_name, not both")
        if info.field_name == "vpc_uuid" and v:
            try:
                UUID4(v)
            except ValueError:
                raise ValueError("Invalid UUID format for VPC")
        return v


class RouterCreate(RouterBase):
    pass


class RouterUpdate(RouterBase):
    pass


class RouterRead(RouterBase):
    id: UUID4 = Field(..., description="Unique identifier for the router")
