from ..credential.service import get_credential_by_id
from .exceptions import CredentialNotFound, DeviceAlreadyExists, DeviceUnableToConnect
from .factory import DeviceFactory
from .schemas import DeviceCreate
from .service import get_device_by_name


async def valid_device_create(data: DeviceCreate):
    if await get_device_by_name(data.name):
        raise DeviceAlreadyExists()

    # Credential validation
    username = None
    password = None
    private_key = None

    if data.credential_id:
        credential = await get_credential_by_id(data.credential_id)
        if not credential:
            raise CredentialNotFound()

        username = credential.username
        password = credential.password
        private_key = credential.private_key

    # Creation of the device instance
    device_instance = DeviceFactory().instance(
        type=data.device_type,
        host=data.host,
        port=data.port,
        protocol=data.protocol,
        username=username,
        password=password,
        private_key=private_key,
        verify=False,  # FIXME
        timeout=10,  # FIXME
    )

    # Connection verification
    if not device_instance.is_connected():
        raise DeviceUnableToConnect()

    return data
