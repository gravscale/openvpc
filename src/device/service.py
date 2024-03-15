from datetime import datetime, timezone

from fastapi import HTTPException
from loguru import logger
from pydantic import UUID4
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from ..config import get_settings
from ..core.netbox_service import NetboxService
from ..credential.models import Credential
from ..zone.models import Zone
from .exceptions import DeviceCreateError, DeviceDeleteError, DeviceNotFound
from .factory import DeviceFactory
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


async def _validate_and_connect_device(data):
    # Validação de zone_uuid e zone_name
    if data.zone_id and data.zone_name:
        raise HTTPException(
            status_code=400, detail="Provide either zone_id or zone_name, not both."
        )

    if not data.zone_id and not data.zone_name:
        raise HTTPException(status_code=400, detail="Provide either zone_id or zone_name.")

    device_exists = await Device.exists(name=data.name, is_active=True)
    if device_exists:
        raise HTTPException(status_code=400, detail="Duplicated device name.")

    zone = await Zone.get_or_none(Q(id=data.zone_id) | Q(name=data.zone_name), is_active=True)
    if not zone:
        raise HTTPException(status_code=404, detail="Zone not found with provided information.")

    # Validação da credencial
    username = None
    password = None
    private_key = None

    if data.credential_id:
        credential = await Credential.get_or_none(id=data.credential_id, is_active=True)
        if not credential:
            raise HTTPException(status_code=404, detail="Credential not found.")

        username = credential.username
        password = credential.password
        private_key = credential.private_key

    # Criação da instância do dispositivo
    device_factory = DeviceFactory()
    device_instance = device_factory.instance(
        type=data.device_type,
        host=data.host,
        port=data.port,
        protocol=data.protocol,
        username=username,
        password=password,
        private_key=private_key,
        verify=False,  # FIXME
        timeout=10,  # FIXME
    )

    # Verificação da conexão
    if not device_instance.is_connected():
        raise HTTPException(status_code=400, detail="Unable to connect to the device.")

    return zone, device_instance


async def create_device(data: DeviceCreate):
    zone, _ = await _validate_and_connect_device(data)

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

    device_dict = data.model_dump()
    device_dict["zone"] = zone
    device_dict["netbox_id"] = netbox_id

    try:
        device = await Device.create(**device_dict)
    except IntegrityError:
        # Delete the device from Netbox
        try:
            await netbox_service.delete_device(netbox_id)
        except HTTPException as e:
            logger.warning(f"Failed to delete device '{data.name}' from Netbox: {e}")

        raise DeviceCreateError()

    return DeviceResponse.model_validate(device)


async def update_device(device_id: UUID4, data: DeviceUpdate):
    pass

    # await validate_uuid(device_id)

    # async with AsyncSessionLocal() as session:
    #     result = await session.execute(
    #         select(Device).where(Device.id == device_id, Device.is_active)
    #     )
    #     device = result.scalars().first()

    #     if not device:
    #         raise HTTPException(status_code=404, detail="Device not found.")

    #     zone, _ = await _validate_and_connect_device(device_data)

    #     update_dict = device_data.model_dump(exclude_unset=True)
    #     update_dict["zone_id"] = zone.id

    #     # Remoção de campos não presentes no modelo Device
    #     update_dict.pop("zone_uuid", None)
    #     update_dict.pop("zone_name", None)

    #     await session.execute(update(Device).where(Device.id == device_id).values(**update_dict))

    #     try:
    #         await session.commit()
    #     except IntegrityError:
    #         await session.rollback()
    #         raise HTTPException(status_code=400, detail="Device update error.")

    #     return await get_device(device_id)


# Async CRUD operation for deleting a device
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
