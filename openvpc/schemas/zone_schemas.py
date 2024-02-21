from datetime import datetime

from pydantic import BaseModel


class ZoneRequest(BaseModel):
    name: str


class ZoneRead(BaseModel):
    id: str
    name: str
    creation_datetime: datetime
    status: bool

    class Config:
        from_attributes = True
