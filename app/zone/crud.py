from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from .model import Zone
from .schema import ZoneCreate, ZoneRead

# from ..config.db import SessionLocal as AsyncSessionLocal
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.future import select


async def list_zone():
    zones = await Zone.filter(is_active=True)
    return [ZoneRead.model_validate(i) for i in zones]

    # async with AsyncSessionLocal() as session:
    #     result = await session.execute(select(Zone).where(Zone.is_active))
    #     return result.scalars().all()


async def create_zone(data: ZoneCreate):
    zone_exists = await Zone.exists(name=data.name, is_active=True)
    if zone_exists:
        raise HTTPException(status_code=400, detail="Duplicated zone name.")

    netbox_id = 1  # FIXME

    try:
        zone = await Zone.create(name=data.name, netbox_id=netbox_id)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Credential create error.")

    return ZoneRead.model_validate(zone)

    # async with AsyncSessionLocal() as session:
    #     # Validação de duplicação de nome
    #     result = await session.execute(select(Zone).where(Zone.name == data.name, Zone.is_active))
    #     zones = result.scalars().all()

    #     if zones:
    #         raise HTTPException(status_code=400, detail="Duplicated zone name.")

    #     zone = Zone(name=data.name, netbox_id=netbox_id)
    #     session.add(zone)

    #     try:
    #         await session.commit()
    #     except IntegrityError:
    #         await session.rollback()
    #         raise HTTPException(status_code=400, detail="Zone create error.")

    #     await session.refresh(zone)
    #     return zone
