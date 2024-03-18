from ..exceptions import BadRequest, NotFound
from ..vpc.constants import ErrorCode as VpcErrorCode
from .constants import ErrorCode


class RouterNotFound(NotFound):
    DETAIL = ErrorCode.ROUTER_NOT_FOUND


class RouterAlreadyExists(BadRequest):
    DETAIL = ErrorCode.ROUTER_ALREADY_EXISTS


class RouterCreateError(BadRequest):
    DETAIL = ErrorCode.ROUTER_CREATE_ERROR


class RouterDeleteError(BadRequest):
    DETAIL = ErrorCode.ROUTER_DELETE_ERROR


class VpcNotFound(BadRequest):
    DETAIL = VpcErrorCode.VPC_NOT_FOUND
