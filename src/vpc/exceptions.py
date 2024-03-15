from ..exceptions import BadRequest, NotFound
from .constants import ErrorCode


class VpcNotFound(NotFound):
    DETAIL = ErrorCode.VPC_NOT_FOUND


class VpcAlreadyExists(BadRequest):
    DETAIL = ErrorCode.VPC_ALREADY_EXISTS


class VpcCreateError(BadRequest):
    DETAIL = ErrorCode.VPC_CREATE_ERROR
