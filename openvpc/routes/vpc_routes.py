from typing import List

from fastapi import APIRouter

from ..crud.vpc_crud import add_vpc, get_vpc
from ..schemas.vpc_schemas import VPCRead, VPCRequest

router = APIRouter()


@router.get("/vpc/", response_model=List[VPCRead], operation_id="vpc-list")
async def list_vpc_endpoint():
    return await get_vpc()


@router.post("/vpc/add", response_model=VPCRead, operation_id="vpc-add")
async def add_vpc_endpoint(vpc_request: VPCRequest):
    return await add_vpc(vpc_request)
