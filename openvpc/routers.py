import importlib
import os

from fastapi import FastAPI


async def include_routers_from_directory(app: FastAPI, directory: str):
    """importar automaticamente todos os routers no diretório de rotas"""

    route_files = [f for f in os.listdir(directory) if f.endswith("_routes.py")]

    for route_file in route_files:
        module_name = os.path.splitext(route_file)[0]
        module = importlib.import_module(f".{directory}.{module_name}", package="openvpc")

        if hasattr(module, "router"):
            app.include_router(module.router)
