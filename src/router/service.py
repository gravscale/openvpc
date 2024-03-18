from datetime import datetime, timezone

from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..vpc.service import get_vpc_by_id, get_vpc_by_name
from .exceptions import (
    RouterCreateError,
    RouterDeleteError,
    RouterNotFound,
    VpcNotFound,
)
from .models import Router
from .schemas import RouterCreate, RouterUpdate


async def get_router_by_id(router_id: UUID4):
    return await Router.get_or_none(id=router_id, is_active=True)


async def get_router_by_name(name: str):
    return await Router.get_or_none(name=name, is_active=True)


async def list_router():
    return await Router.filter(is_active=True)


async def get_router(router_id: UUID4):
    router = await get_router_by_id(router_id)
    if not router:
        raise RouterNotFound()
    return router


async def create_router(data: RouterCreate):
    vpc = None

    if data.vpc_id or data.vpc_name:
        if data.vpc_id:
            vpc = await get_vpc_by_id(data.vpc_id)

        elif data.vpc_name:
            vpc = await get_vpc_by_name(data.vpc_name)

        if not vpc:
            raise VpcNotFound()

    try:
        router = await Router.create(vpc=vpc, **data.model_dump())
    except IntegrityError:
        raise RouterCreateError()

    return router


async def update_router(router_id: UUID4, data: RouterUpdate):
    pass


async def delete_router(router_id: UUID4):
    router = await get_router_by_id(router_id)

    router.is_active = False
    router.deleted_at = datetime.now(timezone.utc)

    try:
        await router.save()
    except IntegrityError:
        raise RouterDeleteError()
