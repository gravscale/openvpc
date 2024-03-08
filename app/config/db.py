from tortoise import Tortoise

from .settings import get_settings

settings = get_settings()


TORTOISE_ORM: dict = {
    "connections": {"default": settings.DB_URL},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "app.zone.model",
                "app.credential.model",
                "app.device.model",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    if settings.TESTING:
        TORTOISE_ORM["connections"]["default"] = settings.DB_TEST_URL

    await Tortoise.init(config=TORTOISE_ORM)

    if settings.TESTING:
        await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
