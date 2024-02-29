from fastapi import HTTPException
from sqlalchemy import update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.future import select

from ..config import get_settings
from ..database import SessionLocal as AsyncSessionLocal
from ..lib.utils import validate_uuid
from ..models.credential_models import Credential
from ..schemas.credential_schemas import CredentialCreate, CredentialUpdate

settings = get_settings()


# Async CRUD operation for listing credentials
async def list_credentials():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(Credential).where(Credential.is_active))
        return result.scalars().all()


# Async CRUD operation for retrieving a credential
async def get_credential(credential_id: str):
    await validate_uuid(credential_id)

    async with AsyncSessionLocal() as session:
        credential = await session.get(Credential, credential_id)
        if not credential:
            raise HTTPException(status_code=404, detail="Credential not found.")
        return credential


# Async CRUD operation for creating a credential
async def create_credential(credential_data: CredentialCreate):
    async with AsyncSessionLocal() as session:
        if credential_data.private_key and credential_data.password:
            raise HTTPException(
                status_code=400, detail="Provide either private_key or password, not both."
            )
        try:
            db_credential = Credential(**credential_data.model_dump())
            session.add(db_credential)
            await session.commit()
            await session.refresh(db_credential)
            return db_credential
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Duplicate credential name.")


# Async CRUD operation for updating a credential
async def update_credential(credential_id: str, credential_data: CredentialUpdate):
    await validate_uuid(credential_id)

    async with AsyncSessionLocal() as session:
        db_credential = await get_credential(credential_id)

        if not db_credential:
            raise HTTPException(status_code=404, detail="Credential not found.")

        if credential_data.private_key and credential_data.password:
            raise HTTPException(
                status_code=400, detail="Provide either private_key or password, not both."
            )

        await session.execute(
            update(Credential)
            .where(Credential.id == credential_id)
            .values(**credential_data.model_dump())
        )

        await session.commit()
        return await get_credential(credential_id)


# Async CRUD operation for deleting a credential
async def delete_credential(credential_id: str):
    await validate_uuid(credential_id)

    async with AsyncSessionLocal() as session:
        db_credential = await get_credential(credential_id)
        if not db_credential:
            raise HTTPException(status_code=404, detail="Credential not found.")

        try:
            await session.delete(db_credential)
            await session.commit()
        except IntegrityError:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Credential delete error.")
