from fastapi import APIRouter, HTTPException
from ..schemas.router_schemas import RouterCreate, RouterRead, RouterUpdate
from ..crud.router_crud import create_router, get_router, update_router, delete_router, list_routers
from typing import List

router = APIRouter()

@router.post("/router", response_model=RouterRead, operation_id="router-add")
async def add_router(router: RouterCreate):
    """
    Creates a new router.
    """
    return await create_router(router)

@router.get("/router/{router_id}", response_model=RouterRead, operation_id="router-get")
async def read_router(router_id: str):
    """
    Retrieves a router by its ID.
    """
    return await get_router(router_id)

@router.put("/router/{router_id}", response_model=RouterRead, operation_id="router-update")
async def modify_router(router_id: str, router: RouterUpdate):
    """
    Updates a specific router.
    """
    return await update_router(router_id, router)

@router.delete("/router/{router_id}", response_model=RouterRead, operation_id="router-del")
async def remove_router(router_id: str):
    """
    Deletes a specific router.
    """
    return await delete_router(router_id)

@router.get("/router", response_model=List[RouterRead], operation_id="router-list")
async def list_all_routers():
    """
    Lists all routers.
    """
    return await list_routers()
