from tortoise.exceptions import IntegrityError

from ..zone.service import get_zone_by_id, get_zone_by_name
from .exceptions import ConfigCreateError, ConfigNotFound, ZoneNotFound
from .models import Config
from .schemas import ConfigSetCreate


async def get_config_by_param(param: str):
    return await Config.get_or_none(param=param)


async def list_config():
    return await Config.all()


async def get_config(param: str):
    config_set = await get_config_by_param(param)
    if not config_set:
        raise ConfigNotFound()
    return config_set


async def config_create(data: ConfigSetCreate):
    scope_zone = None

    if data.scope_zone_id or data.scope_zone_name:
        if data.scope_zone_id:
            scope_zone = await get_zone_by_id(data.scope_zone_id)

        elif data.scope_zone_name:
            scope_zone = await get_zone_by_name(data.scope_zone_name)

        if not scope_zone:
            raise ZoneNotFound()

    try:
        config_set = await Config.create(scope_zone=scope_zone, **data.model_dump())
    except IntegrityError:
        raise ConfigCreateError()

    return config_set
