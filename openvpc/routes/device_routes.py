from typing import List

from fastapi import APIRouter, status

from ..crud.device_crud import (
    create_device,
    delete_device,
    get_device,
    list_devices,
    update_device,
)
from ..schemas.device_schemas import DeviceCreate, DeviceRead, DeviceUpdate

router = APIRouter()


@router.get("/admin/device", response_model=List[DeviceRead], operation_id="admin-device-list")
async def list_all_devices():
    """
    Lists all devices.
    """
    return await list_devices()


@router.get("/admin/device/{device_id}", response_model=DeviceRead, operation_id="admin-device-get")
async def read_device(device_id: str):
    """
    Retrieves a device by its ID.
    """
    return await get_device(device_id)


@router.post(
    "/admin/device",
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="admin-device-add",
)
async def add_device(device: DeviceCreate):
    """
    Creates a new device.
    """
    return await create_device(device)


@router.put(
    "/admin/device/{device_id}", response_model=DeviceRead, operation_id="admin-device-update"
)
async def modify_device(device_id: str, device: DeviceUpdate):
    """
    Updates a specific device.
    """
    return await update_device(device_id, device)


@router.delete(
    "/admin/device/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="admin-device-del",
)
async def remove_device(device_id: str):
    """
    Deletes a specific device.
    """
    await delete_device(device_id)
