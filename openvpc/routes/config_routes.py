from fastapi import APIRouter, HTTPException
from ..schemas.config_schemas import ConfigSetRequest, ConfigRead
from ..crud.config_crud import set_config, get_config, list_configs
from typing import List

router = APIRouter()

@router.post("/admin/config", response_model=ConfigRead, operation_id="admin-config-set")
async def set_config_endpoint(config_request: ConfigSetRequest):
    config_created = await set_config(**config_request.dict())
    return config_created

@router.get("/admin/config/{param}", response_model=ConfigRead, operation_id="admin-config-get")
async def get_config_endpoint(param: str):
    return await get_config(param)

@router.get("/admin/config", response_model=List[ConfigRead], operation_id="admin-config-list")
async def list_configs_endpoint():
    return await list_configs()
