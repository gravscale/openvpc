from pydantic import BaseModel
from datetime import datetime

class VPCRequest(BaseModel):
    primary_device_name: str
    secondary_device_name: str
    name: str

class VPCRead(BaseModel):
    id: str
    name: str
    device_name_primary: str
    device_name_secondary: str
    creation_datetime: datetime
    status: bool

    class Config:
        orm_mode = True