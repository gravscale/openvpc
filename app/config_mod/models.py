from uuid import uuid4

from sqlalchemy import Column, String, UniqueConstraint

from ..database import Base


class Config(Base):
    __tablename__ = "config"
    # Adicionando UniqueConstraint para 'param' e 'scope_zone'
    __table_args__ = (UniqueConstraint("param", "scope_zone", name="_param_scope_zone_uc"),)

    id = Column(String(36), primary_key=True, default=lambda: str(uuid4()), index=True)
    param = Column(String(255), index=True)
    value = Column(String(255))
    format = Column(String(50))  # 'string', 'json', etc.
    scope_zone = Column(
        String(36), nullable=True, index=True
    )  # Opcional: UUID da 'zone' para escopo
