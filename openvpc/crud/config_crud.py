from ..models.config_models import Config
from ..models.zone_models import Zone
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..database import SessionLocal as AsyncSessionLocal
from uuid import UUID
import json

async def get_config(param: str):
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Config).where(Config.param == param))
            config = result.scalars().first()
            if config is None:
                raise HTTPException(status_code=404, detail="Config not found")
            return config
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def set_config(param: str, value: str, format: str = "string", scope_zone: str = None, scope_zone_name: str = None):
    if scope_zone and scope_zone_name:
        raise HTTPException(status_code=400, detail="Only one of scope_zone and scope_zone_name should be provided")

    # Verifica se o valor é um JSON válido se o formato for 'json'
    if format == "json":
        try:
            json.loads(value)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON format")

    async with AsyncSessionLocal() as session:
        # Verifica se a zona existe pelo nome e obtém o UUID correspondente
        if scope_zone_name:
            result = await session.execute(select(Zone).where(Zone.name == scope_zone_name))
            zone = result.scalar_one_or_none()
            if not zone:
                raise HTTPException(status_code=404, detail="Zone not found")
            scope_zone = zone.id  # Usando o UUID da zona

        # Verifica se o UUID da zona é válido e existe
        if scope_zone:
            try:
                UUID(scope_zone)  # Verifica se o scope_zone é um UUID válido
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid scope_zone UUID")

            result = await session.execute(select(Zone).where(Zone.id == scope_zone))
            if not result.scalar_one_or_none():
                raise HTTPException(status_code=404, detail="Zone not found with provided UUID")

        new_config = Config(param=param, value=value, format=format, scope_zone=scope_zone)
        session.add(new_config)
        
        try:
            await session.commit()
            return new_config
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Duplicate configuration for given param and scope_zone")
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))



async def list_configs():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Config))
            configs = result.scalars().all()
            return configs
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
