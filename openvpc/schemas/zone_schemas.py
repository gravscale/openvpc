from pydantic import BaseModel
from datetime import datetime

class ZoneRequest(BaseModel):
    name: str

class ZoneRead(BaseModel):
    id: str
    name: str
    creation_datetime: datetime
    status: bool

    class Config:
        orm_mode = True
