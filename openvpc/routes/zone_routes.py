from typing import List

from fastapi import APIRouter

from ..crud.zone_crud import add_zone, get_zone
from ..schemas.zone_schemas import ZoneRead, ZoneRequest

router = APIRouter()


@router.get("/admin/zone/", response_model=List[ZoneRead], operation_id="admin-zone-list")
async def list_zone_endpoint():
    return await get_zone()


@router.post("/admin/zone/add", response_model=ZoneRead, operation_id="admin-zone-add")
async def add_zone_endpoint(zone_request: ZoneRequest):
    return await add_zone(zone_request)
