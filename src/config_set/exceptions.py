from ..exceptions import BadRequest, NotFound
from ..zone.constants import ErrorCode as ZoneErrorCode
from .constants import ErrorCode


class ConfigNotFound(NotFound):
    DETAIL = ErrorCode.CONFIG_NOT_FOUND


class ConfigAlreadyExists(BadRequest):
    DETAIL = ErrorCode.CONFIG_ALREADY_EXISTS


class ConfigCreateError(BadRequest):
    DETAIL = ErrorCode.CONFIG_CREATE_ERROR


class ZoneNotFound(BadRequest):
    DETAIL = ZoneErrorCode.ZONE_NOT_FOUND
