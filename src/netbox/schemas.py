from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from ..config import get_settings
from ..core.utils import slugify

settings = get_settings()


class NetboxDefaultResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int


class NetboxDeviceCreate(BaseModel):
    name: str
    device_type: int
    site: int
    role: int


class NetboxSiteCreate(BaseModel):
    name: str
    slug: str
    region: int = settings.NETBOX_DEFAULT_SITE_REGION
    group: int = settings.NETBOX_DEFAULT_SITE_GROUP

    @model_validator(mode="before")
    def slugify_name(cls, data: Any) -> Any:
        if isinstance(data, dict):
            data["slug"] = slugify(data.get("name"))
        return data
