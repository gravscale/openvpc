from .exceptions import ConfigAlreadyExists
from .schemas import ConfigCreate
from .service import get_config_by_param


async def valid_config_create(data: ConfigCreate):
    if await get_config_by_param(data.param):
        raise ConfigAlreadyExists()
    return data
