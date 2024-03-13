from .exceptions import VpcAlreadyExists
from .schemas import VpcCreate
from .service import get_vpc_by_name


async def valid_vpc_create(data: VpcCreate):
    if await get_vpc_by_name(data.name):
        raise VpcAlreadyExists()
    return data
