from fastapi import APIRouter, HTTPException
from ..schemas.device_schemas import (
    DeviceCreate, DeviceRead, DeviceUpdate, 
    CredentialCreate, CredentialRead, CredentialUpdate
)
from ..crud.device_crud import (
    create_credential, get_credential, update_credential, 
    delete_credential, list_credentials, 
    create_device, get_device, update_device, 
    delete_device, list_devices
)
from typing import List

router = APIRouter()

# Routes for managing Credentials

@router.post("/admin/credential", response_model=CredentialRead)
async def add_credential(credential: CredentialCreate):
    """
    Creates a new credential.
    """
    return await create_credential(credential)

@router.get("/admin/credential/{credential_id}", response_model=CredentialRead)
async def read_credential(credential_id: str):
    """
    Retrieves a credential by its ID.
    """
    return await get_credential(credential_id)

@router.put("/admin/credential/{credential_id}", response_model=CredentialRead)
async def modify_credential(credential_id: str, credential: CredentialUpdate):
    """
    Updates a specific credential.
    """
    return await update_credential(credential_id, credential)

@router.delete("/admin/credential/{credential_id}", response_model=CredentialRead)
async def remove_credential(credential_id: str):
    """
    Deletes a specific credential.
    """
    return await delete_credential(credential_id)

@router.get("/admin/credential", response_model=List[CredentialRead])
async def list_all_credentials():
    """
    Lists all credentials.
    """
    return await list_credentials()

# Routes for managing Devices

@router.post("/admin/device", response_model=DeviceRead)
async def add_device(device: DeviceCreate):
    """
    Creates a new device.
    """
    return await create_device(device)

@router.get("/admin/device/{device_id}", response_model=DeviceRead)
async def read_device(device_id: str):
    """
    Retrieves a device by its ID.
    """
    return await get_device(device_id)

@router.put("/admin/device/{device_id}", response_model=DeviceRead)
async def modify_device(device_id: str, device: DeviceUpdate):
    """
    Updates a specific device.
    """
    return await update_device(device_id, device)

@router.delete("/admin/device/{device_id}", response_model=DeviceRead)
async def remove_device(device_id: str):
    """
    Deletes a specific device.
    """
    return await delete_device(device_id)

@router.get("/admin/device", response_model=List[DeviceRead])
async def list_all_devices():
    """
    Lists all devices.
    """
    return await list_devices()
