from .exceptions import DeviceAlreadyExists
from .schemas import DeviceCreate
from .service import get_device_by_name


async def valid_device_create(data: DeviceCreate):
    if await get_device_by_name(data.name):
        raise DeviceAlreadyExists()
    return data
