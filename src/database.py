from tortoise import Tortoise

from .config import get_settings

settings = get_settings()


TORTOISE_ORM: dict = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": [
                "aerich.models",
                "src.zone.models",
                "src.credential.models",
                "src.device.models",
                "src.config_set.models",
                "src.vpc.models",
                "src.router.models",
            ],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)

    if settings.ENVIRONMENT.is_testing:
        await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
