from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from .dependencies import valid_router_create
from .schemas import RouterCreate, RouterResponse, RouterUpdate
from .service import (
    create_router,
    delete_router,
    get_router,
    list_router,
    update_router,
)

router = APIRouter()


@router.get(
    "",
    response_model=List[RouterResponse],
    description="Lists all routers.",
    operation_id="router-list",
)
async def list_router_endpoint():
    return await list_router()


@router.get(
    "/{router_id}",
    response_model=RouterResponse,
    description="Retrieves a router by its ID.",
    operation_id="router-get",
)
async def get_router_endpoint(router_id: UUID4):
    return await get_router(router_id)


@router.post(
    "",
    response_model=RouterResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new router.",
    operation_id="router-add",
)
async def create_router_endpoint(data: RouterCreate = [Depends(valid_router_create)]):
    return await create_router(data)


@router.put(
    "/{router_id}",
    response_model=RouterResponse,
    description="Updates a specific router.",
    operation_id="router-update",
)
async def update_router_endpoint(router_id: UUID4, data: RouterUpdate):
    return await update_router(router_id, data)


@router.delete(
    "/{router_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deletes a specific router.",
    operation_id="router-del",
)
async def delete_router_endpoint(router_id: UUID4):
    await delete_router(router_id)
