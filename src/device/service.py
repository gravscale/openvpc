from datetime import datetime, timezone

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..config import get_settings
from ..core.netbox_service import NetboxService
from ..zone.exceptions import ZoneNotFound
from ..zone.service import get_zone_by_id, get_zone_by_name
from .exceptions import DeviceCreateError, DeviceDeleteError, DeviceNotFound
from .models import Device
from .schemas import DeviceCreate, DeviceResponse, DeviceUpdate

settings = get_settings()


async def get_device_by_id(device_id: UUID4):
    return await Device.get_or_none(id=device_id, is_active=True)


async def get_device_by_name(name: str):
    return await Device.get_or_none(name=name, is_active=True)


async def list_device():
    devices = await Device.filter(is_active=True)
    return [DeviceResponse.model_validate(device) for device in devices]


async def get_device(device_id: UUID4):
    zone = await get_device_by_id(device_id)
    if not zone:
        raise DeviceNotFound()
    return DeviceResponse.model_validate(zone)


async def create_device(data: DeviceCreate):
    if data.zone_id:
        zone = await get_zone_by_id(data.zone_id)
    elif data.zone_name:
        zone = await get_zone_by_name(data.zone_name)

    if not zone:
        raise ZoneNotFound()

    # Create the device in Netbox
    netbox_service = NetboxService()
    try:
        netbox_device = netbox_service.create_device(
            device_name=data.name,
            type_id=1,  # FIXME: device_data.device_type,
            site_id=zone.netbox_id,
        )
    except HTTPException as e:
        raise e

    netbox_id = netbox_device["id"]

    try:
        device = await Device.create(zone=zone, netbox_id=netbox_id, **data.model_dump())
    except IntegrityError:
        # Delete the device from Netbox in case of error
        try:
            await netbox_service.delete_device(netbox_id)
        except HTTPException as e:
            logger.error(f"Failed to delete device '{data.name}' from Netbox: {e}")

        raise DeviceCreateError()

    return DeviceResponse.model_validate(device)


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
