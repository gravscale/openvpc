from uuid import uuid4

from sqlalchemy import Boolean, Column, DateTime, String

from ..database import Base


class VPC(Base):
    __tablename__ = "vpc"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    name = Column(String(255), unique=True, index=True)
    device_name_primary = Column(String(255))
    device_name_secondary = Column(String(255))
    creation_datetime = Column(DateTime)
    status = Column(Boolean)
