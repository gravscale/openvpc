import warnings

import httpx
from fastapi import HTTPException

from ..config import get_settings
from .schemas import NetboxDefaultResponse, NetboxDeviceCreate, NetboxSiteCreate

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
settings = get_settings()


class NetboxService:
    def __init__(self):
        self._base_url = settings.NETBOX_URL
        self._headers = {"Authorization": settings.NETBOX_KEY, "Content-Type": "application/json"}

    def create_device(self, data: NetboxDeviceCreate):
        """
        Creates a new device in NetBox.
        """
        r = httpx.post(
            f"{self._base_url}/dcim/devices/",
            json=data.model_dump(),
            headers=self._headers,
        )
        self._handle_response(r)
        return NetboxDefaultResponse.model_validate_json(r.read())

    def delete_device(self, device_id: int):
        """
        Deletes a device from NetBox.
        """
        r = httpx.delete(f"{self._base_url}/dcim/devices/{device_id}/", headers=self._headers)
        self._handle_response(r)

    def create_site(self, data: NetboxSiteCreate):
        """
        Creates a new zone in NetBox.
        """
        r = httpx.post(
            f"{self._base_url}/dcim/sites/",
            json=data.model_dump(),
            headers=self._headers,
        )
        self._handle_response(r)
        return NetboxDefaultResponse.model_validate_json(r.read())

    def _handle_response(self, response):
        """
        Handles HTTP response, raising exceptions for unexpected status codes.
        """
        if response.status_code not in [201, 204]:
            raise HTTPException(status_code=response.status_code, detail=response.json())
