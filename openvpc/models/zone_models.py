from sqlalchemy import Column, String, Boolean, DateTime
from uuid import uuid4
from ..database import Base 


class Zone(Base):
    __tablename__ = "zone"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    name = Column(String(255), unique=True, index=True)
    creation_datetime = Column(DateTime)
    status = Column(Boolean)
