from typing import Optional

from pydantic import BaseModel, Field, ValidationError, model_validator


class ConfigSetRequest(BaseModel):
    model_config = {
        "json_schema_extra": {
            "example": {
                "param": "ipv4_range_vpc",
                "value": "10.0.0.0/16",
                "format": "string",
                "scope_zone": "zone_uuid",
                "scope_zone_name": "zone_name",
            }
        }
    }

    param: str
    value: str
    format: str = "string"
    scope_zone: Optional[str] = Field(default=None)
    scope_zone_name: Optional[str] = Field(default=None)

    @model_validator(mode="before")
    def check_scope(cls, values):
        scope_zone, scope_zone_name = values.get("scope_zone"), values.get("scope_zone_name")
        if scope_zone and scope_zone_name:
            raise ValidationError(
                "Somente um dos campos scope_zone ou scope_zone_name deve ser preenchido."
            )
        return values


class ConfigRead(BaseModel):
    id: str  # Adicionando o campo ID
    param: str
    value: str
    format: str
    scope_zone: Optional[str] = None
