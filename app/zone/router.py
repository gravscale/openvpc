from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from .dependencies import valid_zone_create
from .schemas import ZoneCreate, ZoneResponse
from .service import create_zone, get_zone, list_zone

router = APIRouter()


@router.get(
    "",
    response_model=List[ZoneResponse],
    description="Lists all zones.",
    operation_id="admin-zone-list",
)
async def list_zone_endpoint():
    return await list_zone()


@router.get(
    "/{zone_id}",
    response_model=ZoneResponse,
    description="Retrieves a zone by its ID.",
    operation_id="admin-zone-get",
)
async def get_zone_endpoint(zone_id: UUID4):
    return await get_zone(zone_id)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ZoneResponse,
    dependencies=[Depends(valid_zone_create)],
    description="Creates a new zone.",
    operation_id="admin-zone-add",
)
async def create_zone_endpoint(data: ZoneCreate):
    return await create_zone(data)
