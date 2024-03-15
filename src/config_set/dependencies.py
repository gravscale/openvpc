from .exceptions import ConfigAlreadyExists
from .schemas import ConfigSetCreate
from .service import get_config_by_param


async def valid_config_set(config_set: ConfigSetCreate):
    if await get_config_by_param(config_set.param):
        raise ConfigAlreadyExists()
    return config_set