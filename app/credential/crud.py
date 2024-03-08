from uuid import UUID

from fastapi import HTTPException
from tortoise.exceptions import IntegrityError

from ..config.settings import get_settings

# from ..core.utils import validate_uuid
from .model import Credential
from .schema import CredentialCreate, CredentialRead, CredentialUpdate

# from sqlalchemy import update
# from sqlalchemy.exc import IntegrityError
# from sqlalchemy.future import select

settings = get_settings()


async def _get_obj(credential_id: UUID):
    credential = await Credential.get_or_none(id=credential_id, is_active=True)
    if not credential:
        raise HTTPException(status_code=404, detail="Credential not found.")
    return credential


# Async CRUD operation for listing credentials
async def list_credentials():
    credentials = await Credential.filter(is_active=True)
    return [CredentialRead.model_validate(i) for i in credentials]

    # return (await session.execute(select(Credential).where(Credential.is_active))).scalars().all()


# Async CRUD operation for retrieving a credential
async def get_credential(credential_id: UUID):
    return CredentialRead.model_validate(_get_obj(credential_id))

    # await validate_uuid(credential_id)

    # credential = await db.get(Credential, credential_id)
    # if not credential:
    #     raise HTTPException(status_code=404, detail="Credential not found.")
    # return credential

    # credential = await Credential.get_or_none(id=credential_id)

    # if not credential:
    #     raise HTTPException(status_code=404, detail="Credential not found.")


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

    # try:
    #     db_credential = Credential(**credential_data.model_dump())
    #     db.add(db_credential)
    #     await db.commit()
    #     await db.refresh(db_credential)
    #     return db_credential
    # except IntegrityError:
    #     await db.rollback()
    #     raise HTTPException(status_code=400, detail="Duplicate credential name.")


# Async CRUD operation for updating a credential
async def update_credential(credential_id: UUID, credential_data: CredentialUpdate):
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
async def delete_credential(credential_id: UUID):
    credential = await _get_obj(credential_id)

    try:
        await credential.delete()
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Credential delete error.")

    # await validate_uuid(credential_id)
    # try:
    #     await db.delete(db_credential)
    #     await db.commit()
    # except IntegrityError:
    #     await db.rollback()
    #     raise HTTPException(status_code=400, detail="Credential delete error.")
