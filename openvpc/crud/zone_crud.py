from fastapi import HTTPException
from sqlalchemy.future import select

from ..database import SessionLocal as AsyncSessionLocal
from ..models.zone_models import Zone
from ..schemas.zone_schemas import ZoneCreate


async def get_zone():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Zone))
            zone = result.scalars().all()
            return zone
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def add_zone(data: ZoneCreate):
    netbox_id = 1  # FIXME

    async with AsyncSessionLocal() as session:
        new_zone = Zone(name=data.name, netbox_id=netbox_id)
        session.add(new_zone)

        try:
            await session.commit()
            return new_zone
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
