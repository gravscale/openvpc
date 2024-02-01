from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from uuid import uuid4
from ..database import Base  

class Router(Base):
    __tablename__ = "router"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    name = Column(String(255), unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    # assocation with VPC (using UUID String)
    vpc_uuid = Column(String(36), ForeignKey('vpc.id'), nullable=True)

    # vpc relationship
    vpc = relationship("VPC", backref="router")




