from ..exceptions import BadRequest, NotFound
from .constants import ErrorCode


class DeviceNotFound(NotFound):
    DETAIL = ErrorCode.DEVICE_NOT_FOUND


class DeviceAlreadyExists(BadRequest):
    DETAIL = ErrorCode.DEVICE_ALREADY_EXISTS


class DeviceCreateError(BadRequest):
    DETAIL = ErrorCode.DEVICE_CREATE_ERROR


class DeviceDeleteError(BadRequest):
    DETAIL = ErrorCode.DEVICE_DELETE_ERROR
