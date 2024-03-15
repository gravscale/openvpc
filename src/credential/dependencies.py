from .exceptions import CredentialAlreadyExists
from .schemas import CredentialCreate
from .service import get_credential_by_name


async def valid_credential_create(data: CredentialCreate):
    if await get_credential_by_name(data.name):
        raise CredentialAlreadyExists()
    return data
