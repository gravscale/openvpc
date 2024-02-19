import os

from fastapi import APIRouter, HTTPException

from ..devices.factory import Device_Factory

router = APIRouter()


@router.get("/test")
async def test():
    kw = {
        "type": "vyos",
        "protocol": "http",
        "host": os.environ.get("VYOS_HOST"),
        "port": os.environ.get("VYOS_PORT"),
        "username": os.environ.get("VYOS_USERNAME"),
        "password": os.environ.get("VYOS_PASSWORD"),
    }
    factory = Device_Factory().instance(**kw)
    return factory.is_connected()
