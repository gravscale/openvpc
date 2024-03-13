from datetime import datetime

from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from ..core.utils import validate_uuid
from ..database import SessionLocal as AsyncSessionLocal
from .models import Router
from .schemas import RouterCreate, RouterUpdate


# Async CRUD operation for creating a router
async def create_router(router_data: RouterCreate):
    async with AsyncSessionLocal() as session:
        if router_data.vpc_uuid and router_data.vpc_name:
            raise HTTPException(
                status_code=400, detail="Provide either vpc_uuid or vpc_name, not both."
            )
        if router_data.vpc_uuid:
            await validate_uuid(router_data.vpc_uuid)

        try:
            db_router = Router(**router_data.model_dump())
            session.add(db_router)
            await session.commit()
            await session.refresh(db_router)
            return db_router
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Duplicate router name.")


# Async CRUD operation for retrieving a router
async def get_router(router_id: str):
    await validate_uuid(router_id)
    async with AsyncSessionLocal() as session:
        router = await session.get(Router, router_id)
        if not router:
            raise HTTPException(status_code=404, detail="Router not found.")
        return router


# Async CRUD operation for updating a router
async def update_router(router_id: str, router_data: RouterUpdate):
    await validate_uuid(router_id)
    async with AsyncSessionLocal() as session:
        db_router = await get_router(router_id)
        if not db_router:
            raise HTTPException(status_code=404, detail="Router not found.")

        await session.execute(
            update(Router).where(Router.id == router_id).values(**router_data.model_dump())
        )
        await session.commit()
        return await get_router(router_id)


# Async CRUD operation for deleting a router
async def delete_router(router_id: str):
    await validate_uuid(router_id)
    async with AsyncSessionLocal() as session:
        db_router = await get_router(router_id)
        if not db_router:
            raise HTTPException(status_code=404, detail="Router not found.")
        # Update status and deletion time of the router
        db_router.is_active = False
        db_router.deleted_at = datetime.utcnow()
        await session.commit()
        return db_router


# Async CRUD operation for listing routers
async def list_routers():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Router).where(Router.is_active))
        return result.scalars().all()
