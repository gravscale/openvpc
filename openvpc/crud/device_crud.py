# device_crud.py
from ..models.device_models import Device, Credential
from ..models.zone_models import Zone
from ..schemas.device_schemas import DeviceCreate, DeviceUpdate, CredentialCreate, CredentialUpdate
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from ..database import SessionLocal as AsyncSessionLocal
from uuid import UUID
from datetime import datetime

# Helper function to validate UUID format
async def validate_uuid(uuid_str: str):
    try:
        UUID(uuid_str)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid UUID format.")


# Async CRUD operation for creating a device
async def create_device(device_data: DeviceCreate):
    async with AsyncSessionLocal() as session:
        # Handle zone_uuid and zone_name validations
        if device_data.zone_uuid and device_data.zone_name:
            raise HTTPException(status_code=400, detail="Provide either zone_uuid or zone_name, not both.")
        if not device_data.zone_uuid and not device_data.zone_name:
            raise HTTPException(status_code=400, detail="Provide either zone_uuid or zone_name.")

        # Validate and fetch Zone
        if device_data.zone_uuid:
            await validate_uuid(device_data.zone_uuid)
            zone = await session.get(Zone, device_data.zone_uuid)
            if not zone:
                raise HTTPException(status_code=404, detail="Zone not found with provided UUID.")
        elif device_data.zone_name:
            result = await session.execute(select(Zone).where(Zone.name == device_data.zone_name))
            zone = result.scalars().first()
            if not zone:
                raise HTTPException(status_code=404, detail="Zone not found with provided name.")
        device_data.zone_id = zone.id  # Assign zone UUID to device

        # Validate Credential
        if device_data.credential_id:
            await validate_uuid(device_data.credential_id)
            credential = await get_credential(device_data.credential_id)
            if not credential:
                raise HTTPException(status_code=404, detail="Credential not found.")

        try:
            db_device = Device(**device_data.dict())
            session.add(db_device)
            await session.commit()
            await session.refresh(db_device)
            return db_device
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Duplicate device name.")

# Async CRUD operation for retrieving a device
async def get_device(device_id: str):
    await validate_uuid(device_id)
    async with AsyncSessionLocal() as session:
        device = await session.get(Device, device_id)
        if not device:
            raise HTTPException(status_code=404, detail="Device not found.")
        return device

# Async CRUD operation for updating a device
async def update_device(device_id: str, device_data: DeviceUpdate):
    await validate_uuid(device_id)
    async with AsyncSessionLocal() as session:
        db_device = await get_device(device_id)
        if not db_device:
            raise HTTPException(status_code=404, detail="Device not found.")
        if device_data.credential_id:
            await validate_uuid(device_data.credential_id)
            credential = await get_credential(device_data.credential_id)
            if not credential:
                raise HTTPException(status_code=404, detail="Credential not found.")
        await session.execute(
            update(Device).where(Device.id == device_id).values(**device_data.dict())
        )
        await session.commit()
        return await get_device(device_id)

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
        result = await session.execute(select(Device).where(Device.is_active == True))
        return result.scalars().all()



# Async CRUD operation for creating a credential
async def create_credential(credential_data: CredentialCreate):
    async with AsyncSessionLocal() as session:
        if credential_data.private_key and credential_data.password:
            raise HTTPException(status_code=400, detail="Provide either private_key or password, not both.")
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
            raise HTTPException(status_code=400, detail="Provide either private_key or password, not both.")
        await session.execute(
            update(Credential).where(Credential.id == credential_id).values(**credential_data.dict())
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
