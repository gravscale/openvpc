from .exceptions import ZoneAlreadyExists
from .schemas import ZoneCreate
from .service import get_zone_by_name


async def valid_zone_create(zone: ZoneCreate):
    if await get_zone_by_name(zone.name):
        raise ZoneAlreadyExists()
    return zone
