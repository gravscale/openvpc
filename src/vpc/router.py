from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from .dependencies import valid_vpc_create
from .schemas import VpcCreate, VpcResponse
from .service import create_vpc, get_vpc, list_vpc

router = APIRouter()


@router.get(
    "",
    response_model=List[VpcResponse],
    description="Lists all VPCs.",
    operation_id="vpc-list",
)
async def list_vpc_endpoint():
    return await list_vpc()


@router.get(
    "/{vpc_id}",
    response_model=VpcResponse,
    description="Retrieves a VPC by its ID.",
    operation_id="vpc-get",
)
async def get_vpc_endpoint(vpc_id: UUID4):
    return await get_vpc(vpc_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=VpcResponse,
    description="Creates a new VPC.",
    operation_id="vpc-add",
)
async def create_vpc_endpoint(data: VpcCreate = Depends(valid_vpc_create)):
    return await create_vpc(data)
