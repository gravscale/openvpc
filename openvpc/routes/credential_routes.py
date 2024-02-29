from typing import List

from fastapi import APIRouter, status

from ..crud.credential_crud import (
    create_credential,
    delete_credential,
    get_credential,
    list_credentials,
    update_credential,
)
from ..schemas.credential_schemas import (
    CredentialCreate,
    CredentialRead,
    CredentialUpdate,
)

router = APIRouter()


@router.get(
    "/admin/credential", response_model=List[CredentialRead], operation_id="admin-credential-list"
)
async def list_all_credentials():
    """
    Lists all credentials.
    """
    return await list_credentials()


@router.get(
    "/admin/credential/{credential_id}",
    response_model=CredentialRead,
    operation_id="admin-credential-get",
)
async def read_credential(credential_id: str):
    """
    Retrieves a credential by its ID.
    """
    return await get_credential(credential_id)


@router.post(
    "/admin/credential",
    response_model=CredentialRead,
    status_code=status.HTTP_201_CREATED,
    operation_id="admin-credential-add",
)
async def add_credential(credential: CredentialCreate):
    """
    Creates a new credential.
    """
    return await create_credential(credential)


@router.put(
    "/admin/credential/{credential_id}",
    response_model=CredentialRead,
    operation_id="admin-credential-update",
)
async def modify_credential(credential_id: str, credential: CredentialUpdate):
    """
    Updates a specific credential.
    """
    return await update_credential(credential_id, credential)


@router.delete(
    "/admin/credential/{credential_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    operation_id="admin-credential-del",
)
async def remove_credential(credential_id: str):
    """
    Deletes a specific credential.
    """
    await delete_credential(credential_id)
