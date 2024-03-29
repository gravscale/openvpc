from tortoise.exceptions import IntegrityError

from ..zone.service import get_zone_by_id, get_zone_by_name
from .exceptions import ConfigCreateError, ConfigNotFound, ZoneNotFound
from .models import Config
from .schemas import ConfigCreate


async def get_config_by_param(param: str):
    return await Config.get_or_none(param=param)


async def list_config():
    return await Config.all()


async def get_config(param: str):
    config = await get_config_by_param(param)
    if not config:
        raise ConfigNotFound()
    return config


async def config_create(data: ConfigCreate):
    dump = data.model_dump()
    scope_zone = None

    if data.scope_zone_id or data.scope_zone_name:
        if data.scope_zone_id:
            scope_zone = await get_zone_by_id(data.scope_zone_id)

        elif data.scope_zone_name:
            scope_zone = await get_zone_by_name(data.scope_zone_name)

        if not scope_zone:
            raise ZoneNotFound()

        dump["scope_zone"] = scope_zone

    dump.pop("scope_zone_id")
    dump.pop("scope_zone_name")

    try:
        config = await Config.create(**dump)
    except IntegrityError:
        raise ConfigCreateError()

    return config
