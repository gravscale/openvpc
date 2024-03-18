from ..credential.constants import ErrorCode as CredentialErrorCode
from ..exceptions import BadRequest, NotFound
from ..zone.constants import ErrorCode as ZoneErrorCode
from .constants import ErrorCode


class DeviceNotFound(NotFound):
    DETAIL = ErrorCode.DEVICE_NOT_FOUND


class DeviceAlreadyExists(BadRequest):
    DETAIL = ErrorCode.DEVICE_ALREADY_EXISTS


class DeviceCreateError(BadRequest):
    DETAIL = ErrorCode.DEVICE_CREATE_ERROR


class DeviceDeleteError(BadRequest):
    DETAIL = ErrorCode.DEVICE_DELETE_ERROR


class DeviceUnableToConnect(BadRequest):
    DETAIL = ErrorCode.DEVICE_UNABLE_TO_CONNECT


class ZoneNotFound(BadRequest):
    DETAIL = ZoneErrorCode.ZONE_NOT_FOUND


class CredentialNotFound(BadRequest):
    DETAIL = CredentialErrorCode.CREDENTIAL_NOT_FOUND
