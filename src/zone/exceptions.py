from ..exceptions import BadRequest, NotFound
from .constants import ErrorCode


class ZoneNotFound(NotFound):
    DETAIL = ErrorCode.ZONE_NOT_FOUND


class ZoneAlreadyExists(BadRequest):
    DETAIL = ErrorCode.ZONE_ALREADY_EXISTS


class ZoneCreateError(BadRequest):
    DETAIL = ErrorCode.ZONE_CREATE_ERROR
