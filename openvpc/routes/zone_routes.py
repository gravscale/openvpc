from fastapi import APIRouter
from ..schemas.zone_schemas import ZoneRead, ZoneRequest
from ..crud.zone_crud import get_zone, add_zone
from typing import List

router = APIRouter()

@router.get("/admin/zone/", response_model=List[ZoneRead])
async def list_zone_endpoint():
    return await get_zone()

@router.post("/admin/zone/add", response_model=ZoneRead)
async def add_zone_endpoint(zone_request: ZoneRequest):
    return await add_zone(zone_request)
