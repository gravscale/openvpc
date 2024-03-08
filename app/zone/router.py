from typing import List

from fastapi import APIRouter, status

from .crud import create_zone, list_zone
from .schema import ZoneCreate, ZoneRead

router = APIRouter()


@router.get("", response_model=List[ZoneRead], operation_id="admin-zone-list")
async def list_zone_endpoint():
    return await list_zone()


@router.post(
    "", response_model=ZoneRead, status_code=status.HTTP_201_CREATED, operation_id="admin-zone-add"
)
async def create_zone_endpoint(data: ZoneCreate):
    return await create_zone(data)
