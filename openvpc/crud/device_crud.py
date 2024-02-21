# device_crud.py
from datetime import datetime
from uuid import UUID

from devices.factory import DeviceFactory
from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from ..database import SessionLocal as AsyncSessionLocal
from ..models.device_models import Credential, Device
from ..models.zone_models import Zone
from ..schemas.device_schemas import (
    CredentialCreate,
    CredentialUpdate,
    DeviceCreate,
    DeviceUpdate,
)


# Helper function to validate UUID format
async def validate_uuid(uuid_str: str):
    try:
        UUID(uuid_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")


# Async CRUD operation for retrieving a device
async def get_device(device_id: str):
    await validate_uuid(device_id)
    async with AsyncSessionLocal() as session:
        device = await session.get(Device, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found.")
        return device


# Async CRUD operation for deleting a device
async def delete_device(device_id: str):
    await validate_uuid(device_id)
    async with AsyncSessionLocal() as session:
        db_device = await get_device(device_id)
        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found.")
        # Update status and deletion time of the device
        db_device.is_active = False
        db_device.deleted_at = datetime.utcnow()
        await session.commit()
        return db_device


# Async CRUD operation for listing devices
async def list_devices():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Device).where(Device.is_active))
        return result.scalars().all()


# Async CRUD operation for creating a credential
async def create_credential(credential_data: CredentialCreate):
    async with AsyncSessionLocal() as session:
        if credential_data.private_key and credential_data.password:
            raise HTTPException(
                status_code=400, detail="Provide either private_key or password, not both."
            )
        try:
            db_credential = Credential(**credential_data.dict())
            session.add(db_credential)
            await session.commit()
            await session.refresh(db_credential)
            return db_credential
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Duplicate credential name.")


# Async CRUD operation for retrieving a credential
async def get_credential(credential_id: str):
    await validate_uuid(credential_id)
    async with AsyncSessionLocal() as session:
        credential = await session.get(Credential, credential_id)
        if not credential:
            raise HTTPException(status_code=404, detail="Credential not found.")
        return credential


# Async CRUD operation for updating a credential
async def update_credential(credential_id: str, credential_data: CredentialUpdate):
    await validate_uuid(credential_id)
    async with AsyncSessionLocal() as session:
        db_credential = await get_credential(credential_id)
        if not db_credential:
            raise HTTPException(status_code=404, detail="Credential not found.")
        if credential_data.private_key and credential_data.password:
            raise HTTPException(
                status_code=400, detail="Provide either private_key or password, not both."
            )
        await session.execute(
            update(Credential)
            .where(Credential.id == credential_id)
            .values(**credential_data.dict())
        )
        await session.commit()
        return await get_credential(credential_id)


# Async CRUD operation for deleting a credential
async def delete_credential(credential_id: str):
    await validate_uuid(credential_id)
    async with AsyncSessionLocal() as session:
        db_credential = await get_credential(credential_id)
        if not db_credential:
            raise HTTPException(status_code=404, detail="Credential not found.")
        await session.delete(db_credential)
        await session.commit()
        return db_credential


# Async CRUD operation for listing credentials
async def list_credentials():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Credential))
        return result.scalars().all()


async def validate_and_connect_device(device_data, credential_id):
    async with AsyncSessionLocal() as session:
        # Validação de zone_uuid e zone_name
        if device_data.zone_id and device_data.zone_name:
            raise HTTPException(
                status_code=400, detail="Provide either zone_id or zone_name, not both."
            )
        if not device_data.zone_id and not device_data.zone_name:
            raise HTTPException(status_code=400, detail="Provide either zone_id or zone_name.")

        # Validação e obtenção do Zone ID
        zone_id = None
        if device_data.zone_id:
            await validate_uuid(device_data.zone_id)
            zone = await session.get(Zone, device_data.zone_id)
            if zone:
                zone_id = zone.id
        elif device_data.zone_name:
            result = await session.execute(select(Zone).where(Zone.name == device_data.zone_name))
            zone = result.scalars().first()
            if zone:
                zone_id = zone.id
        if not zone_id:
            raise HTTPException(status_code=404, detail="Zone not found with provided information.")

        # Validação da credencial
        if credential_id:
            await validate_uuid(credential_id)
            credential = await get_credential(credential_id)
            if not credential:
                raise HTTPException(status_code=404, detail="Credential not found.")

        # Criação da instância do dispositivo
        device_factory = DeviceFactory()
        device_instance = device_factory.instance(
            type=device_data.device_type,
            host=device_data.host,
            port=device_data.port,
            protocol=device_data.protocol,
            username=credential.user,
            password=credential.password,
            private_key=credential.private_key,
            verify=False,  # FIXME
            timeout=10,  # FIXME
        )

        # Verificação da conexão
        if not device_instance.is_connected():
            raise HTTPException(status_code=400, detail="Unable to connect to the device.")

        return zone_id, device_instance


async def create_device(device_data: DeviceCreate):
    zone_id, device_instance = await validate_and_connect_device(
        device_data, device_data.credential_id
    )

    async with AsyncSessionLocal() as session:
        try:
            device_dict = device_data.dict()
            device_dict["zone_id"] = zone_id

            # Remoção de campos não presentes no modelo Device
            device_dict.pop("zone_uuid", None)
            device_dict.pop("zone_name", None)

            db_device = Device(**device_dict)
            session.add(db_device)
            await session.commit()
            await session.refresh(db_device)
            return db_device
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Duplicate device name.")


async def update_device(device_id: str, device_data: DeviceUpdate):
    await validate_uuid(device_id)

    async with AsyncSessionLocal() as session:
        db_device = await get_device(device_id)
        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found.")

        zone_id, device_instance = await validate_and_connect_device(
            device_data, device_data.credential_id
        )

        try:
            update_dict = device_data.dict(exclude_unset=True)
            update_dict["zone_id"] = zone_id

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
            raise HTTPException(status_code=400, detail="Error updating device.")
