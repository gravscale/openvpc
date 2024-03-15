from datetime import datetime, timezone

from pydantic import UUID4
from tortoise.exceptions import IntegrityError

from ..config import get_settings
from .exceptions import CredentialCreateError, CredentialDeleteError, CredentialNotFound
from .models import Credential
from .schemas import CredentialCreate, CredentialResponse, CredentialUpdate

settings = get_settings()


async def get_credential_by_id(credential_id: UUID4):
    return await Credential.get_or_none(id=credential_id, is_active=True)


async def get_credential_by_name(name: UUID4):
    return await Credential.get_or_none(name=name, is_active=True)


async def list_credential():
    credentials = await Credential.filter(is_active=True)
    return [CredentialResponse.model_validate(i) for i in credentials]


async def get_credential(credential_id: UUID4):
    credential = await get_credential_by_id(credential_id)
    if not credential:
        raise CredentialNotFound()
    return CredentialResponse.model_validate(credential)


async def create_credential(data: CredentialCreate):
    try:
        credential = await Credential.create(**data.model_dump())
    except IntegrityError:
        raise CredentialCreateError()

    return CredentialResponse.model_validate(credential)


async def update_credential(credential_id: UUID4, data: CredentialUpdate):
    pass


async def delete_credential(credential_id: UUID4):
    credential = await get_credential_by_id(credential_id)

    credential.is_active = False
    credential.deleted_at = datetime.now(timezone.utc)

    try:
        await credential.save()
    except IntegrityError:
        raise CredentialDeleteError()
