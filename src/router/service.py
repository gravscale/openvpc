from datetime import datetime, timezone

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..config import get_settings
from ..netbox.schemas import NetboxDeviceCreate
from ..netbox.service import NetboxService
from ..vpc.service import get_vpc_by_id, get_vpc_by_name
from .exceptions import (
    RouterCreateError,
    RouterDeleteError,
    RouterNotFound,
    VpcNotFound,
)
from .models import Router
from .schemas import RouterCreate, RouterUpdate

settings = get_settings()


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
    dump = data.model_dump()
    vpc = None

    if data.vpc_id or data.vpc_name:
        if data.vpc_id:
            vpc = await get_vpc_by_id(data.vpc_id)

        elif data.vpc_name:
            vpc = await get_vpc_by_name(data.vpc_name)

        if not vpc:
            raise VpcNotFound()

        dump["vpc"] = vpc

    dump.pop("vpc_id")
    dump.pop("vpc_name")

    # Create the device in Netbox
    netbox_service = NetboxService()

    try:
        netbox_device = netbox_service.create_device(
            NetboxDeviceCreate(
                name=data.name,
                device_type=1,  # FIXME: device_data.device_type,
                site=1,  # FIXME: zone?,
                role=settings.NETBOX_ROUTER_ROLE,
            )
        )
    except HTTPException as e:
        raise e

    netbox_id = netbox_device.id
    dump["netbox_id"] = netbox_id

    # Create the router in the database
    try:
        router = await Router.create(**dump)
    except IntegrityError:
        # Delete the device from Netbox in case of error
        try:
            netbox_service.delete_device(netbox_id)
        except HTTPException as e:
            logger.error(f"Failed to delete device '{data.name}' from Netbox: {e}")

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
