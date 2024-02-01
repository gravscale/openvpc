from fastapi import FastAPI
from .database import engine, Base
import os
import importlib

app = FastAPI()

# importar automaticamente todos os routers no diretório de rotas
def include_routers_from_directory(directory: str):
    for filename in os.listdir(directory):
        if filename.endswith("_routes.py"):
            module_name_short = filename.replace('_routes.py', '')
            module_name_full = f"routes.{module_name_short}_routes"
            module_name_partial = f"{module_name_short}_routes"

            #print("routes filename: ", filename)
            #print("routes module_name_short: ", module_name_short)
            #print("routes module_name_partial: ", module_name_partial)
            #print("routes module_name_full: ", module_name_full)

            module = importlib.import_module(f".{module_name_full}", package="openvpc")
            router = getattr(module, "router", None)
            if router:
                app.include_router(router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# Inclui automaticamente todos os routers da pasta de rotas
include_routers_from_directory("routes")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("openvpc.main:app", host="0.0.0.0", port=8000, reload=True)
