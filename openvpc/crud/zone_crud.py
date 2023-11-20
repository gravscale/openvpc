from ..models.zone_models import Zone
from sqlalchemy.future import select
from fastapi import HTTPException
from ..database import SessionLocal as AsyncSessionLocal
from ..schemas.zone_schemas import ZoneRequest
from datetime import datetime

async def get_zone():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(Zone))
            zone = result.scalars().all()
            return zone
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

async def add_zone(zone_request: ZoneRequest):
    async with AsyncSessionLocal() as session:
        new_zone = Zone(
            name=zone_request.name,
            creation_datetime=datetime.now(),
            status=True
        )
        session.add(new_zone)
        try:
            await session.commit()
            return new_zone
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
