from fastapi import FastAPI

from app.credential import router as credential_router
from app.device import router as device_router
from app.zone import router as zone_router

# config_router,; device_router,; router_router,; vpc_router,; ,


def init_routers(app: FastAPI):
    @app.get("/healthcheck", include_in_schema=False)
    async def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    app.include_router(credential_router.router, prefix="/admin/credential")
    app.include_router(zone_router.router, prefix="/admin/zone")
    app.include_router(device_router.router, prefix="/admin/device")
    # app.include_router(config_router.router, prefix="/admin/configuration")
    # app.include_router(router_router.router, prefix="/router")
    # app.include_router(vpc_router.router, prefix="/vpc")
