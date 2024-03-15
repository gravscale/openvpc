from typing import List

from fastapi import APIRouter, Depends, status
from pydantic import UUID4

from .dependencies import valid_credential_create
from .schemas import CredentialCreate, CredentialResponse, CredentialUpdate
from .service import (
    create_credential,
    delete_credential,
    get_credential,
    list_credential,
    update_credential,
)

router = APIRouter()


@router.get(
    "",
    response_model=List[CredentialResponse],
    description="Lists all credentials.",
    operation_id="admin-credential-list",
)
async def list_credential_endpoint():
    return await list_credential()


@router.get(
    "/{credential_id}",
    response_model=CredentialResponse,
    description="Retrieves a credential by its ID.",
    operation_id="admin-credential-get",
)
async def get_credential_endpoint(credential_id: UUID4):
    return await get_credential(credential_id)


@router.post(
    "",
    response_model=CredentialResponse,
    status_code=status.HTTP_201_CREATED,
    description="Creates a new credential.",
    operation_id="admin-credential-add",
)
async def create_credential_endpoint(
    credential: CredentialCreate = [Depends(valid_credential_create)],
):
    return await create_credential(credential)


@router.put(
    "/{credential_id}",
    response_model=CredentialResponse,
    description="Updates a specific credential.",
    operation_id="admin-credential-update",
)
async def update_credential_endpoint(credential_id: UUID4, credential: CredentialUpdate):
    return await update_credential(credential_id, credential)


@router.delete(
    "/{credential_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Deletes a specific credential.",
    operation_id="admin-credential-del",
)
async def delete_credential_endpoint(credential_id: UUID4):
    await delete_credential(credential_id)
