# from uuid import uuid4

# from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
# from sqlalchemy.orm import relationship
# from sqlalchemy.sql import func

# from ..config.db import Base

# class Device(Base):
#     __tablename__ = "device"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
#     name = Column(String(255), index=True)
#     device_type = Column(String(255))
#     host = Column(String(255))
#     port = Column(Integer)
#     protocol = Column(String(50))
#     netbox_id = Column(Integer)
#     zone_id = Column(String(36), ForeignKey("zone.id"))
#     credential_id = Column(String(36), ForeignKey("credential.id"))
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     deleted_at = Column(DateTime(timezone=True), nullable=True)

#     # Relacionamentos
#     credential = relationship("Credential")
#     zone = relationship("Zone")

from tortoise import fields, models


class Device(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    device_type = fields.CharField(max_length=255)
    host = fields.CharField(max_length=255)
    port = fields.IntField()
    protocol = fields.CharField(max_length=50)
    netbox_id = fields.IntField()
    zone = fields.ForeignKeyField("models.Zone", related_name="devices")
    credential = fields.ForeignKeyField("models.Credential", null=True, related_name="devices")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "device"
        ordering = ["created_at"]