from datetime import datetime, timezone

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..config import get_settings
from ..netbox.schemas import NetboxDeviceCreate
from ..netbox.service import NetboxService
from ..zone.service import get_zone_by_id, get_zone_by_name
from .exceptions import (
    DeviceCreateError,
    DeviceDeleteError,
    DeviceNotFound,
    ZoneNotFound,
)
from .models import Device
from .schemas import DeviceCreate, DeviceUpdate

settings = get_settings()


async def get_device_by_id(device_id: UUID4):
    return await Device.get_or_none(id=device_id, is_active=True)


async def get_device_by_name(name: str):
    return await Device.get_or_none(name=name, is_active=True)


async def list_device():
    return await Device.filter(is_active=True)


async def get_device(device_id: UUID4):
    device = await get_device_by_id(device_id)
    if not device:
        raise DeviceNotFound()
    return device


async def create_device(data: DeviceCreate):
    if data.zone_id:
        zone = await get_zone_by_id(data.zone_id)
    elif data.zone_name:
        zone = await get_zone_by_name(data.zone_name)

    if not zone:
        raise ZoneNotFound()

    dump = data.model_dump()
    dump["zone"] = zone
    dump.pop("zone_id")
    dump.pop("zone_name")

    # Create the device in Netbox
    netbox_service = NetboxService()

    try:
        netbox_device = netbox_service.create_device(
            NetboxDeviceCreate(
                name=data.name,
                device_type=1,  # FIXME: device_data.device_type,
                site=zone.netbox_id,
                role=settings.NETBOX_DEVICE_ROLE,
            )
        )
    except HTTPException as e:
        raise e

    netbox_id = netbox_device.id
    dump["netbox_id"] = netbox_id

    # Create the device in the database
    try:
        device = await Device.create(**dump)
    except IntegrityError:
        # Delete the device from Netbox in case of error
        try:
            netbox_service.delete_device(netbox_id)
        except HTTPException as e:
            logger.error(f"Failed to delete device '{data.name}' from Netbox: {e}")

        raise DeviceCreateError()

    return device


async def update_device(device_id: UUID4, data: DeviceUpdate):
    pass


async def delete_device(device_id: UUID4):
    device = await get_device_by_id(device_id)

    # Delete the device from Netbox
    try:
        NetboxService().delete_device(device.netbox_id)
    except HTTPException as e:
        raise e

    # Delete the device in the database
    device.is_active = False
    device.deleted_at = datetime.now(timezone.utc)

    try:
        await device.save()
    except IntegrityError:
        raise DeviceDeleteError()
