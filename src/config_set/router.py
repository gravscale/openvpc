from typing import List

from fastapi import APIRouter, Depends, status

from .dependencies import valid_config_create
from .schemas import ConfigSetCreate, ConfigSetResponse
from .service import config_create, get_config, list_config

router = APIRouter()


@router.get(
    "",
    response_model=List[ConfigSetResponse],
    description="Lists all configs.",
    operation_id="admin-config-list",
)
async def list_config_endpoint():
    return await list_config()


@router.get(
    "/{param}",
    response_model=ConfigSetResponse,
    description="Retrieves a config by its param.",
    operation_id="admin-config-get",
)
async def get_config_endpoint(param: str):
    return await get_config(param)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ConfigSetResponse,
    description="Sets a config.",
    operation_id="admin-config-set",
)
async def config_create_endpoint(data: ConfigSetCreate = Depends(valid_config_create)):
    return await config_create(data)
