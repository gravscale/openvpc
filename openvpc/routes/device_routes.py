from typing import List

from fastapi import APIRouter

from ..crud.device_crud import (
    create_credential,
    create_device,
    delete_credential,
    delete_device,
    get_credential,
    get_device,
    list_credentials,
    list_devices,
    update_credential,
    update_device,
)
from ..schemas.device_schemas import (
    CredentialCreate,
    CredentialRead,
    CredentialUpdate,
    DeviceCreate,
    DeviceRead,
    DeviceUpdate,
)

router = APIRouter()

# Routes for managing Credentials


@router.post(
    "/admin/credential", response_model=CredentialRead, operation_id="admin-credential-add"
)
async def add_credential(credential: CredentialCreate):
    """
    Creates a new credential.
    """
    return await create_credential(credential)


@router.get(
    "/admin/credential/{credential_id}",
    response_model=CredentialRead,
    operation_id="admin-credential-get",
)
async def read_credential(credential_id: str):
    """
    Retrieves a credential by its ID.
    """
    return await get_credential(credential_id)


@router.put(
    "/admin/credential/{credential_id}",
    response_model=CredentialRead,
    operation_id="admin-credential-update",
)
async def modify_credential(credential_id: str, credential: CredentialUpdate):
    """
    Updates a specific credential.
    """
    return await update_credential(credential_id, credential)


@router.delete(
    "/admin/credential/{credential_id}",
    response_model=CredentialRead,
    operation_id="admin-credential-del",
)
async def remove_credential(credential_id: str):
    """
    Deletes a specific credential.
    """
    return await delete_credential(credential_id)


@router.get(
    "/admin/credential", response_model=List[CredentialRead], operation_id="admin-credential-list"
)
async def list_all_credentials():
    """
    Lists all credentials.
    """
    return await list_credentials()


# Routes for managing Devices
@router.post("/admin/device", response_model=DeviceRead, operation_id="admin-device-add")
async def add_device(device: DeviceCreate):
    """
    Creates a new device.
    """
    return await create_device(device)


@router.get("/admin/device/{device_id}", response_model=DeviceRead, operation_id="admin-device-get")
async def read_device(device_id: str):
    """
    Retrieves a device by its ID.
    """
    return await get_device(device_id)


@router.put(
    "/admin/device/{device_id}", response_model=DeviceRead, operation_id="admin-device-update"
)
async def modify_device(device_id: str, device: DeviceUpdate):
    """
    Updates a specific device.
    """
    return await update_device(device_id, device)


@router.delete(
    "/admin/device/{device_id}", response_model=DeviceRead, operation_id="admin-device-del"
)
async def remove_device(device_id: str):
    """
    Deletes a specific device.
    """
    return await delete_device(device_id)


@router.get("/admin/device", response_model=List[DeviceRead], operation_id="admin-device-list")
async def list_all_devices():
    """
    Lists all devices.
    """
    return await list_devices()
