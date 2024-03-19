import json
from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import (
    UUID4,
    BaseModel,
    ConfigDict,
    Field,
    field_validator,
    model_validator,
)

from ..core.utils import slugify
from .constants import ErrorCode


class Format(str, Enum):
    string = "string"
    json = "json"


class ConfigBase(BaseModel):
    param: str = Field(..., description="Unique name for the config")
    value: str = Field(..., description="Value of the config")
    format: Format = Field(Format.string, description="Format of the value: string, json")
    scope_zone_id: Optional[UUID4] = Field(default=None, description="UUID of the associated zone")
    scope_zone_name: Optional[str] = Field(default=None, description="Name of the associated zone")


class ConfigCreate(ConfigBase):
    @model_validator(mode="after")
    def check_scope_zone(self):
        if self.scope_zone_id and self.scope_zone_name:
            raise ValueError(ErrorCode.ZONE_ID_AND_NAME_PROVIDED)
        return self

    @model_validator(mode="after")
    def check_json_format(self):
        if self.format == "json":
            try:
                json.loads(self.value)
            except json.JSONDecodeError:
                raise ValueError(ErrorCode.INVALID_JSON_FORMAT)
        return self

    @field_validator("param")
    @classmethod
    def slugify_param(cls, v: str):
        return slugify(v)


class ConfigResponse(ConfigBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID4 = Field(..., description="Unique identifier for the config")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
