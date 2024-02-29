from typing import List

from fastapi import APIRouter

from ..crud.zone_crud import add_zone, get_zone
from ..schemas.zone_schemas import ZoneCreate, ZoneRead

router = APIRouter()


@router.get("/admin/zone", response_model=List[ZoneRead], operation_id="admin-zone-list")
async def list_zone_endpoint():
    return await get_zone()


@router.post("/admin/zone", response_model=ZoneRead, operation_id="admin-zone-add")
async def add_zone_endpoint(data: ZoneCreate):
    return await add_zone(data)
