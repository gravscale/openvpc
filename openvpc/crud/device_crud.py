from datetime import datetime

from devices.factory import DeviceFactory
from fastapi import HTTPException
from loguru import logger
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from ..config import get_settings
from ..crud.credential_crud import get_credential
from ..database import SessionLocal as AsyncSessionLocal
from ..lib.netbox import NetboxHelper
from ..lib.utils import validate_uuid
from ..models.device_models import Device
from ..models.zone_models import Zone
from ..schemas.device_schemas import DeviceCreate, DeviceUpdate

settings = get_settings()


# Async CRUD operation for listing devices
async def list_devices():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Device).where(Device.is_active))
        return result.scalars().all()


# Async CRUD operation for retrieving a device
async def get_device(device_id: str):
    await validate_uuid(device_id)

    async with AsyncSessionLocal() as session:
        device = await session.get(Device, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found.")

        return device


async def _validate_and_connect_device(device_data, credential_id=None):
    async with AsyncSessionLocal() as session:
        # Validação de zone_uuid e zone_name
        if device_data.zone_id and device_data.zone_name:
            raise HTTPException(
                status_code=400, detail="Provide either zone_id or zone_name, not both."
            )
        if not device_data.zone_id and not device_data.zone_name:
            raise HTTPException(status_code=400, detail="Provide either zone_id or zone_name.")

        # Validação e obtenção do Zone ID
        zone = None

        if device_data.zone_id:
            await validate_uuid(device_data.zone_id)
            zone = await session.get(Zone, device_data.zone_id)

        elif device_data.zone_name:
            result = await session.execute(select(Zone).where(Zone.name == device_data.zone_name))
            zone = result.scalars().first()

        if not zone:
            raise HTTPException(status_code=404, detail="Zone not found with provided information.")

        # Validação da credencial
        if credential_id:
            await validate_uuid(credential_id)
            credential = await get_credential(credential_id)

            if not credential:
                raise HTTPException(status_code=404, detail="Credential not found.")

            username = credential.user
            password = credential.password
            private_key = credential.private_key

        # Criação da instância do dispositivo
        device_factory = DeviceFactory()
        device_instance = device_factory.instance(
            type=device_data.device_type,
            host=device_data.host,
            port=device_data.port,
            protocol=device_data.protocol,
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


async def create_device(device_data: DeviceCreate):
    zone, _ = await _validate_and_connect_device(device_data, device_data.credential_id)

    # Tenta criar o dispositivo no NetBox
    netbox_helper = NetboxHelper()
    try:
        device_netbox = await netbox_helper.create_device(
            device_name=device_data.name,
            type_id=1,  # FIXME: device_data.device_type,
            site_id=zone.netbox_id,
        )
    except HTTPException as e:
        raise e

    device_netbox_id = device_netbox["id"]

    device_dict = device_data.model_dump()
    device_dict["zone_id"] = zone.id
    device_dict["netbox_id"] = device_netbox_id

    # Remoção de campos não presentes no modelo Device
    device_dict.pop("zone_uuid", None)
    device_dict.pop("zone_name", None)

    async with AsyncSessionLocal() as session:
        device = Device(**device_dict)
        session.add(device)

        try:
            await session.commit()
        except IntegrityError:
            await session.rollback()

            # Tenta remover o dispositivo criado no NetBox, se possível
            try:
                await netbox_helper.delete_device(device_netbox_id)
            except Exception as e:
                logger.warning(f"Failed to delete device from netbox {device_data.name}: {e}")

            raise HTTPException(status_code=400, detail="Device create error.")

        await session.refresh(device)
        return device


async def update_device(device_id: str, device_data: DeviceUpdate):
    await validate_uuid(device_id)

    async with AsyncSessionLocal() as session:
        db_device = await get_device(device_id)

        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found.")

        zone, _ = await _validate_and_connect_device(device_data, device_data.credential_id)

        try:
            update_dict = device_data.model_dump(exclude_unset=True)
            update_dict["zone_id"] = zone.id

            # Remoção de campos não presentes no modelo Device
            update_dict.pop("zone_uuid", None)
            update_dict.pop("zone_name", None)

            await session.execute(
                update(Device).where(Device.id == device_id).values(**update_dict)
            )
            await session.commit()
            return await get_device(device_id)
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Device update error.")


# Async CRUD operation for deleting a device
async def delete_device(device_id: str):
    await validate_uuid(device_id)

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Device).where(Device.id == device_id, Device.is_active)
        )
        device = result.scalars().first()

        if not device:
            raise HTTPException(status_code=404, detail="Device not found.")

        # Tenta excluir o dispositivo no NetBox
        netbox_helper = NetboxHelper()
        try:
            await netbox_helper.delete_device(device.netbox_id)
        except HTTPException as e:
            raise e

        # Update status and deletion time of the device
        device.is_active = False
        device.deleted_at = datetime.utcnow()
        await session.commit()
