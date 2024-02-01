from sqlalchemy import Column, String, ForeignKey, DateTime, Integer, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from uuid import uuid4
from ..database import Base  

class Credential(Base):
    __tablename__ = "credential"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    name = Column(String(255), unique=True, index=True)
    user = Column(String(255))
    private_key = Column(String(2048), nullable=True)
    password = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

class Device(Base):
    __tablename__ = "device"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    name = Column(String(255), unique=True, index=True)
    device_type = Column(String(255))
    host = Column(String(255))
    port = Column(Integer)
    protocol = Column(String(50))
    zone_id = Column(String(36), ForeignKey('zone.id'))
    credential_id = Column(String(36), ForeignKey('credential.id'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True)

    # Relacionamentos
    credential = relationship("Credential")
    zone = relationship("Zone")