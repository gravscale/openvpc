from tortoise.exceptions import IntegrityError

from ..zone.exceptions import ZoneNotFound
from ..zone.service import get_zone_by_id, get_zone_by_name
from .exceptions import ConfigCreateError, ConfigNotFound
from .models import Config
from .schemas import ConfigResponse, ConfigSetRequest


async def get_config_by_param(param: str):
    return await Config.get_or_none(param=param)


async def list_config():
    configs = await Config.all()
    return [ConfigResponse.model_validate(config) for config in configs]


async def get_config(param: str):
    config = await get_config_by_param(param)
    if not config:
        raise ConfigNotFound()
    return ConfigResponse.model_validate(config)


async def set_config(config_set: ConfigSetRequest):
    scope_zone = None

    if config_set.scope_zone_id or config_set.scope_zone_name:
        if config_set.scope_zone_id:
            scope_zone = await get_zone_by_id(config_set.scope_zone_id)

        elif config_set.scope_zone_name:
            scope_zone = await get_zone_by_name(config_set.scope_zone_name)

        if not scope_zone:
            raise ZoneNotFound()

    try:
        config = await Config.create(scope_zone=scope_zone, **config_set.model_dump())
    except IntegrityError:
        raise ConfigCreateError()

    return ConfigResponse.model_validate(config)
