from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..core.netbox_service import NetboxService
from .exceptions import ZoneCreateError, ZoneNotFound
from .models import Zone
from .schemas import ZoneCreate


async def get_zone_by_id(zone_id: UUID4):
    return await Zone.get_or_none(id=zone_id, is_active=True)


async def get_zone_by_name(name: str):
    return await Zone.get_or_none(name=name, is_active=True)


async def list_zone():
    return await Zone.filter(is_active=True)


async def get_zone(zone_id: UUID4):
    zone = await get_zone_by_id(zone_id)
    if not zone:
        raise ZoneNotFound()
    return zone


async def create_zone(data: ZoneCreate):
    # Create the zone in Netbox
    netbox_service = NetboxService()
    try:
        netbox_zone = netbox_service.create_zone(name=data.name)
    except Exception as e:
        raise e

    netbox_id = netbox_zone["id"]

    # Create the zone in the database
    try:
        zone = await Zone.create(netbox_id=netbox_id, **data.model_dump())
    except IntegrityError:
        raise ZoneCreateError()

    return zone
