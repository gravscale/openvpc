from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field, model_validator

from .constants import ErrorCode


class RouterBase(BaseModel):
    name: str = Field(..., description="Unique name for the router")
    vpc_id: Optional[UUID4] = Field(None, description="UUID of the associated VPC")
    vpc_name: Optional[str] = Field(None, description="Name of the associated VPC")


class RouterCreate(RouterBase):
    @model_validator(mode="after")
    def check_vpc_id_or_name(self):
        if self.vpc_id and self.vpc_name:
            raise ValueError(ErrorCode.ROUTER_VPC_ID_OR_NAME_ERROR)
        return self


class RouterUpdate(RouterCreate):
    pass


class RouterResponse(RouterBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the router")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
