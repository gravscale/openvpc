from fastapi import HTTPException
from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..config import get_settings
from .models import Credential
from .schemas import CredentialCreate, CredentialRead, CredentialUpdate

settings = get_settings()


async def _get_obj(credential_id: UUID4):
    credential = await Credential.get_or_none(id=credential_id, is_active=True)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found.")
    return credential


# Async CRUD operation for listing credentials
async def list_credentials():
    credentials = await Credential.filter(is_active=True)
    return [CredentialRead.model_validate(i) for i in credentials]


# Async CRUD operation for retrieving a credential
async def get_credential(credential_id: UUID4):
    return CredentialRead.model_validate(await _get_obj(credential_id))


# Async CRUD operation for creating a credential
async def create_credential(data: CredentialCreate):
    if data.private_key and data.password:
        raise HTTPException(
            status_code=400, detail="Provide either private_key or password, not both."
        )

    credential_exists = await Credential.exists(name=data.name, is_active=True)
    if credential_exists:
        raise HTTPException(status_code=400, detail="Duplicated credential name.")

    try:
        credential = await Credential.create(**data.model_dump())
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Credential create error.")

    return CredentialRead.model_validate(credential)


# Async CRUD operation for updating a credential
async def update_credential(credential_id: UUID4, credential_data: CredentialUpdate):
    pass

    # await validate_uuid(credential_id)

    # db_credential = await get_credential(credential_id)

    # if not db_credential:
    #     raise HTTPException(status_code=404, detail="Credential not found.")

    # if credential_data.private_key and credential_data.password:
    #     raise HTTPException(
    #         status_code=400, detail="Provide either private_key or password, not both."
    #     )

    # await session.execute(
    #     update(Credential)
    #     .where(Credential.id == credential_id)
    #     .values(**credential_data.model_dump())
    # )

    # await session.commit()
    # return await get_credential(credential_id)


# Async CRUD operation for deleting a credential
async def delete_credential(credential_id: UUID4):
    credential = await _get_obj(credential_id)

    try:
        await credential.delete()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Credential delete error.")
