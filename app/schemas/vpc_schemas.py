from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VPCRequest(BaseModel):
    primary_device_name: str
    secondary_device_name: str
    name: str


class VPCRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    device_name_primary: str
    device_name_secondary: str
    creation_datetime: datetime
    status: bool
