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
            ],
            "default_connection": "default",
        },
    },
}


async def init_db() -> None:
    await Tortoise.init(config=TORTOISE_ORM)


async def init_test_db() -> None:
    TORTOISE_ORM["connections"]["default"] = settings.DB_TEST_URL
    await init_db()
    await Tortoise.generate_schemas()


async def close_db() -> None:
    await Tortoise.close_connections()
