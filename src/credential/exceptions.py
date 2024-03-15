from ..exceptions import BadRequest, NotFound
from .constants import ErrorCode


class CredentialNotFound(NotFound):
    DETAIL = ErrorCode.CREDENTIAL_NOT_FOUND


class CredentialAlreadyExists(BadRequest):
    DETAIL = ErrorCode.CREDENTIAL_ALREADY_EXISTS


class CredentialCreateError(BadRequest):
    DETAIL = ErrorCode.CREDENTIAL_CREATE_ERROR


class CredentialDeleteError(BadRequest):
    DETAIL = ErrorCode.CREDENTIAL_DELETE_ERROR
