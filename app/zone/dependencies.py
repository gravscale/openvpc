from pydantic import UUID4

from .exceptions import ZoneNameAlreadyExists, ZoneNotFound
from .schemas import ZoneCreate
from .service import get_zone_by_id, get_zone_by_name


async def valid_zone_get(zone_id: UUID4):
    if not await get_zone_by_id(zone_id):
        raise ZoneNotFound()
    return zone_id


async def valid_zone_create(zone: ZoneCreate):
    if await get_zone_by_name(zone.name):
        raise ZoneNameAlreadyExists()
    return zone
