# from uuid import uuid4

# from ..config.db import Base

# from sqlalchemy import Boolean, Column, DateTime, Integer, String
# from sqlalchemy.sql import func


# class Zone(Base):
#     __tablename__ = "zone"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
#     name = Column(String(255), unique=True, index=True)
#     netbox_id = Column(Integer)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     deleted_at = Column(DateTime(timezone=True), nullable=True)

from tortoise import fields, models


class Zone(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    netbox_id = fields.IntField()
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "zone"
        ordering = ["created_at"]
