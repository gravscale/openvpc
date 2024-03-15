from ..exceptions import BadRequest, NotFound
from .constants import ErrorCode


class RouterNotFound(NotFound):
    DETAIL = ErrorCode.ROUTER_NOT_FOUND


class RouterAlreadyExists(BadRequest):
    DETAIL = ErrorCode.ROUTER_ALREADY_EXISTS


class RouterCreateError(BadRequest):
    DETAIL = ErrorCode.ROUTER_CREATE_ERROR


class RouterDeleteError(BadRequest):
    DETAIL = ErrorCode.ROUTER_DELETE_ERROR
