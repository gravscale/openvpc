# from uuid import uuid4

# from sqlalchemy import Boolean, Column, DateTime, String
# from sqlalchemy.sql import func

# from ..config.db import Base


# class Credential(Base):
#     __tablename__ = "credential"

#     id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
#     name = Column(String(255), index=True)
#     user = Column(String(255))
#     private_key = Column(String(2048), nullable=True)
#     password = Column(String(255), nullable=True)
#     is_active = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())
#     updated_at = Column(DateTime(timezone=True), onupdate=func.now())
#     deleted_at = Column(DateTime(timezone=True), nullable=True)

from tortoise import fields, models


class Credential(models.Model):
    id = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=255, index=True)
    username = fields.CharField(max_length=255)
    password = fields.CharField(max_length=255, null=True)
    private_key = fields.CharField(max_length=2048, null=True)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
    deleted_at = fields.DatetimeField(null=True)

    class Meta:
        table = "credential"
        ordering = ["created_at"]
