from .exceptions import ZoneAlreadyExists
from .schemas import ZoneCreate
from .service import get_zone_by_name


async def valid_zone_create(data: ZoneCreate):
    if await get_zone_by_name(data.name):
        raise ZoneAlreadyExists()
    return data
