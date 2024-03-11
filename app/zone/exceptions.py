from app.exceptions import BadRequest, NotFound


class ZoneNotFound(NotFound):
    DETAIL = "Zone not found."


class ZoneNameAlreadyExists(BadRequest):
    DETAIL = "Zone name already exists."


class ZoneCreateError(BadRequest):
    DETAIL = "Zone create error."
