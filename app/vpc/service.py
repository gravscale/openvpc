from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from .exceptions import VpcCreateError
from .models import Vpc
from .schemas import VpcCreate, VpcResponse


async def get_vpc_by_name(vpc_name: str):
    return await Vpc.get_or_none(name=vpc_name, is_active=True)


async def list_vpc():
    vpcs = await Vpc.filter(is_active=True)
    return [VpcResponse.model_validate(vpc) for vpc in vpcs]


async def get_vpc(vpc_id: UUID4):
    return await Vpc.get_or_none(id=vpc_id, is_active=True)


async def create_vpc(data: VpcCreate):
    try:
        vpc = await Vpc.create(**data.model_dump())
    except IntegrityError:
        raise VpcCreateError()

    return VpcResponse.model_validate(vpc)
