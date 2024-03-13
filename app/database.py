from tortoise import Tortoise

from .config import get_settings

settings = get_settings()


TORTOISE_ORM: dict = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "app.zone.models",
                "app.credential.models",
                "app.device.models",
                "app.configuration.models",
                "app.vpc.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)

    if settings.TESTING:
        await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
