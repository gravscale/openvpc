from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from loguru import logger
from tortoise.exceptions import IntegrityError
from tortoise.expressions import Q

from ..config.settings import get_settings
from ..credential.model import Credential
from ..services.netbox_service import NetboxService
from ..zone.model import Zone
from .factory import DeviceFactory
from .model import Device
from .schema import DeviceCreate, DeviceRead, DeviceUpdate

settings = get_settings()


async def _get_obj(id_: UUID):
    device = await Device.get_or_none(id=id_, is_active=True)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found.")
    return device


# Async CRUD operation for listing devices
async def list_devices():
    devices = await Device.filter(is_active=True)
    return [DeviceRead.model_validate(i) for i in devices]

    # async with AsyncSessionLocal() as session:
    #     result = await session.execute(select(Device).where(Device.is_active))
    #     return result.scalars().all()


# Async CRUD operation for retrieving a device
async def get_device(id_: UUID):
    return DeviceRead.model_validate(_get_obj(id_))

    # await validate_uuid(device_id)

    # async with AsyncSessionLocal() as session:
    #     device = await session.get(Device, device_id)
    #     if not device:
    #         raise HTTPException(status_code=404, detail="Device not found.")

    #     return device


async def _validate_and_connect_device(data):
    # Validação de zone_uuid e zone_name
    if data.zone_id and data.zone_name:
        raise HTTPException(
            status_code=400, detail="Provide either zone_id or zone_name, not both."
        )

    if not data.zone_id and not data.zone_name:
        raise HTTPException(status_code=400, detail="Provide either zone_id or zone_name.")

    # Validação de duplicação de nome de dispositivo
    # result = await session.execute(select(Device).where(Device.name == data.name,
    # Device.is_active))
    # devices = result.scalars().all()

    device_exists = await Device.exists(name=data.name, is_active=True)
    if device_exists:
        raise HTTPException(status_code=400, detail="Duplicated device name.")

    # Validação e obtenção do Zone ID
    # zone = None

    # if data.zone_id:
    #     # await validate_uuid(data.zone_id)
    #     # result = await session.execute(select(Zone).where(Zone.id == data.zone_id,
    # Zone.is_active))
    #     # zone = result.scalars().first()
    #     zone = await Zone.get(id=data.zone_id, is_active=True)

    # elif data.zone_name:
    #     # result = await session.execute(
    #     #     select(Zone).where(Zone.name == data.zone_name, Zone.is_active)
    #     # )
    #     # zone = result.scalars().first()
    #     zone = await Zone.get(name=data.zone_name, is_active=True)

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

    # Tenta criar o dispositivo no NetBox
    netbox_service = NetboxService()

    try:
        device_netbox = await netbox_service.create_device(
            device_name=data.name,
            type_id=1,  # FIXME: device_data.device_type,
            site_id=zone.netbox_id,
        )
    except HTTPException as e:
        raise e

    device_netbox_id = device_netbox["id"]

    device_dict = data.model_dump()
    device_dict["zone_id"] = zone.id
    device_dict["netbox_id"] = device_netbox_id

    # Remoção de campos não presentes no modelo Device
    device_dict.pop("zone_uuid", None)
    device_dict.pop("zone_name", None)

    try:
        device = await Device.create(**device_dict)
    except IntegrityError:
        # await session.rollback()

        # Tenta remover o dispositivo criado no NetBox, se possível
        try:
            await netbox_service.delete_device(device_netbox_id)
        except Exception as e:
            logger.warning(f"Failed to delete device from netbox {data.name}: {e}")

        raise HTTPException(status_code=400, detail="Device create error.")

    return DeviceRead.model_validate(device)

    # zone, _ = await _validate_and_connect_device(device_data)

    # # Tenta criar o dispositivo no NetBox
    # netbox_service = NetboxService()
    # try:
    #     device_netbox = await netbox_service.create_device(
    #         device_name=device_data.name,
    #         type_id=1,  # FIXME: device_data.device_type,
    #         site_id=zone.netbox_id,
    #     )
    # except HTTPException as e:
    #     raise e

    # device_netbox_id = device_netbox["id"]

    # device_dict = device_data.model_dump()
    # device_dict["zone_id"] = zone.id
    # device_dict["netbox_id"] = device_netbox_id

    # # Remoção de campos não presentes no modelo Device
    # device_dict.pop("zone_uuid", None)
    # device_dict.pop("zone_name", None)

    # async with AsyncSessionLocal() as session:
    #     device = Device(**device_dict)
    #     session.add(device)

    #     try:
    #         await session.commit()
    #     except IntegrityError:
    #         await session.rollback()

    #         # Tenta remover o dispositivo criado no NetBox, se possível
    #         try:
    #             await netbox_service.delete_device(device_netbox_id)
    #         except Exception as e:
    #             logger.warning(f"Failed to delete device from netbox {device_data.name}: {e}")

    #         raise HTTPException(status_code=400, detail="Device create error.")

    #     await session.refresh(device)
    #     return device


async def update_device(id_: UUID, data: DeviceUpdate):
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
async def delete_device(id_: UUID):
    device = await _get_obj(id_)

    # try:
    #     await device.delete()
    # except IntegrityError:
    #     raise HTTPException(status_code=400, detail="Device delete error.")

    # await validate_uuid(device_id)

    # async with AsyncSessionLocal() as session:
    #     result = await session.execute(
    #         select(Device).where(Device.id == device_id, Device.is_active)
    #     )
    #     device = result.scalars().first()

    #     if not device:
    #         raise HTTPException(status_code=404, detail="Device not found.")

    # Tenta excluir o dispositivo no NetBox
    try:
        await NetboxService().delete_device(device.netbox_id)
    except HTTPException as e:
        raise e

    device.is_active = False
    device.deleted_at = datetime.utcnow()

    try:
        await device.save()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Device delete error.")

    #     # Update status and deletion time of the device
    #     device.is_active = False
    #     device.deleted_at = datetime.utcnow()
    #     await session.commit()
