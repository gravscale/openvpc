from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.future import select

from ..database import SessionLocal as AsyncSessionLocal
from ..models.vpc_models import VPC
from ..schemas.vpc_schemas import VPCRequest


async def get_vpc():
    async with AsyncSessionLocal() as session:
        try:
            result = await session.execute(select(VPC))
            vpc = result.scalars().all()
            return vpc
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


async def add_vpc(vpc_request: VPCRequest):
    async with AsyncSessionLocal() as session:
        new_vpc = VPC(
            name=vpc_request.name,
            device_name_primary=vpc_request.primary_device_name,
            device_name_secondary=vpc_request.secondary_device_name,
            creation_datetime=datetime.now(),
            status=True,
        )
        session.add(new_vpc)
        try:
            await session.commit()
            return new_vpc
        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=str(e))
