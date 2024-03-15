from .exceptions import RouterAlreadyExists
from .schemas import RouterCreate
from .service import get_router_by_name


async def valid_router_create(data: RouterCreate):
    if await get_router_by_name(data.name):
        raise RouterAlreadyExists()
    return data
