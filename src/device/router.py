from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from .dependencies import valid_device_create
from .schemas import DeviceCreate, DeviceResponse, DeviceUpdate
from .service import (
    create_device,
    delete_device,
    get_device,
    list_device,
    update_device,
)

router = APIRouter()


@router.get(
    "",
    response_model=List[DeviceResponse],
    description="Lists all devices.",
    operation_id="admin-device-list",
)
async def list_devices_endpoint():
    return await list_device()


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    description="Retrieves a device by its ID.",
    operation_id="admin-device-get",
)
async def get_device_endpoint(device_id: UUID4):
    return await get_device(device_id)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new device.",
    operation_id="admin-device-add",
)
async def create_device_endpoint(data: DeviceCreate = Depends(valid_device_create)):
    return await create_device(data)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    description="Updates a specific device.",
    operation_id="admin-device-update",
)
async def update_device_endpoint(device_id: UUID4, data: DeviceUpdate):
    return await update_device(device_id, data)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deletes a specific device.",
    operation_id="admin-device-del",
)
async def delete_device_endpoint(device_id: UUID4):
    await delete_device(device_id)
