from typing import List

from fastapi import APIRouter, status

from .crud import create_device, delete_device, get_device, list_devices, update_device
from .schema import DeviceCreate, DeviceRead, DeviceUpdate

router = APIRouter()


@router.get("", response_model=List[DeviceRead], operation_id="admin-device-list")
async def list_devices_endpoint():
    return await list_devices()


@router.post(
    "",
    response_model=DeviceRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="admin-device-add",
)
async def create_device_endpoint(device: DeviceCreate):
    return await create_device(device)


@router.get("/{device_id}", response_model=DeviceRead, operation_id="admin-device-get")
async def get_device_endpoint(device_id: str):
    return await get_device(device_id)


@router.put("/{device_id}", response_model=DeviceRead, operation_id="admin-device-update")
async def update_device_endpoint(device_id: str, device: DeviceUpdate):
    return await update_device(device_id, device)


@router.delete(
    "/{device_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="admin-device-del"
)
async def delete_device_endpoint(device_id: str):
    await delete_device(device_id)
