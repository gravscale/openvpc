from fastapi import FastAPI

from app.credential import router as credential_router
from app.device import router as device_router
from app.zone import router as zone_router

# config_router,; device_router,; router_router,; vpc_router,; ,


async def init_routers(app: FastAPI):
    @app.get("/healthz")
    async def health_check():
        return {"Health": True}

    app.include_router(credential_router.router, prefix="/admin/credential")
    app.include_router(zone_router.router, prefix="/admin/zone")
    app.include_router(device_router.router, prefix="/admin/device")
    # app.include_router(config_router.router, prefix="/admin/config")
    # app.include_router(router_router.router, prefix="/router")
    # app.include_router(vpc_router.router, prefix="/vpc")


# async def include_routers_from_directory(app: FastAPI, directory: str):
#     """importar automaticamente todos os routers no diretório de rotas"""

#     route_files = [f for f in os.listdir(directory) if f.endswith("_routes.py")]

#     for route_file in route_files:
#         module_name = os.path.splitext(route_file)[0]
#         module = importlib.import_module(f".{directory}.{module_name}", package="app")

#         if hasattr(module, "router"):
#             app.include_router(module.router)
