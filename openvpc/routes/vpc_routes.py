from fastapi import APIRouter
from ..schemas.vpc_schemas import VPCRead, VPCRequest
from ..crud.vpc_crud import get_vpc, add_vpc
from typing import List

router = APIRouter()

@router.get("/vpc/", response_model=List[VPCRead])
async def list_vpc_endpoint():
    return await get_vpc()

@router.post("/vpc/add", response_model=VPCRead)
async def add_vpc_endpoint(vpc_request: VPCRequest):
    return await add_vpc(vpc_request)

