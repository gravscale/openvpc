import os

import requests
from fastapi import APIRouter, HTTPException

from ..devices.factory import Device_Factory

router = APIRouter()


@router.get("/test")
async def test():
    # kw = {
    #     "type": "vyos",
    #     "protocol": "https",
    #     "host": os.environ.get("VYOS_HOST"),
    #     "port": os.environ.get("VYOS_PORT"),
    #     "username": os.environ.get("VYOS_USERNAME"),
    #     "password": os.environ.get("VYOS_PASSWORD"),
    # }
    # factory = Device_Factory().instance(**kw)
    # return factory.is_connected()

    url = "http://192.168.0.18:2081/retrieve"
    payload = {
        "data": '{"op": "showConfig", "path": []}',
        "key": "vyos",
    }
    headers = {}
    response = requests.post(url, data=payload, headers=headers)
    print(response.text)
