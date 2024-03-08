import warnings

import requests
from fastapi import HTTPException

from ..config.settings import get_settings

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
settings = get_settings()


class NetboxService:
    def __init__(self):
        self._root_url = settings.NETBOX_URL
        self._headers = {"Authorization": settings.NETBOX_KEY, "Content-Type": "application/json"}

    async def create_device(
        self,
        device_name: str,
        type_id: int,
        site_id: int,
        role_id: int = settings.NETBOX_DEFAULT_ROLE,
    ):
        """
        Creates a new device in NetBox.
        """
        r = requests.post(
            f"{self._root_url}/dcim/devices/",
            json={
                "name": device_name,
                "device_type": type_id,
                "role": role_id,
                "site": site_id,
            },
            headers=self._headers,
        )
        await self._handle_response(r)
        return r.json()

    async def delete_device(self, device_id: int):
        """
        Deletes a device from NetBox.
        """
        r = requests.delete(f"{self._root_url}/dcim/devices/{device_id}/", headers=self._headers)
        await self._handle_response(r)

    async def _handle_response(self, response):
        """
        Handles HTTP response, raising exceptions for unexpected status codes.
        """
        if response.status_code not in [201, 204]:
            raise HTTPException(status_code=response.status_code, detail=response.text)
