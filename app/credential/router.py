from typing import List

from fastapi import APIRouter, status
from pydantic import UUID4

from .schemas import CredentialCreate, CredentialRead, CredentialUpdate
from .service import (
    create_credential,
    delete_credential,
    get_credential,
    list_credentials,
    update_credential,
)

router = APIRouter()


@router.get("", response_model=List[CredentialRead], operation_id="admin-credential-list")
async def list_credentials_endpoint():
    """
    Lists all credentials.
    """
    return await list_credentials()


@router.post(
    "",
    response_model=CredentialRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="admin-credential-add",
)
async def create_credential_endpoint(credential: CredentialCreate):
    """
    Creates a new credential.
    """
    return await create_credential(credential)


@router.get(
    "/{credential_id}",
    response_model=CredentialRead,
    operation_id="admin-credential-get",
)
async def get_credential_endpoint(credential_id: UUID4):
    """
    Retrieves a credential by its ID.
    """
    return await get_credential(credential_id)


@router.put(
    "/{credential_id}", response_model=CredentialRead, operation_id="admin-credential-update"
)
async def update_credential_endpoint(credential_id: UUID4, credential: CredentialUpdate):
    """
    Updates a specific credential.
    """
    return await update_credential(credential_id, credential)


@router.delete(
    "/{credential_id}", status_code=status.HTTP_204_NO_CONTENT, operation_id="admin-credential-del"
)
async def delete_credential_endpoint(credential_id: UUID4):
    """
    Deletes a specific credential.
    """
    await delete_credential(credential_id)
