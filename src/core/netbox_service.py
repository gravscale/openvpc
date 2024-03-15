import warnings

import httpx
from fastapi import HTTPException

from ..config import get_settings
from ..core.utils import slugify

warnings.filterwarnings("ignore", message="Unverified HTTPS request")
settings = get_settings()


class NetboxService:
    def __init__(self):
        self._base_url = settings.NETBOX_URL
        self._headers = {"Authorization": settings.NETBOX_KEY, "Content-Type": "application/json"}

    def create_device(
        self,
        name: str,
        type_id: int,
        site_id: int,
        role_id: int = settings.NETBOX_DEFAULT_DEVICE_ROLE,
    ):
        """
        Creates a new device in NetBox.
        """
        r = httpx.post(
            f"{self._base_url}/dcim/devices/",
            json={"name": name, "device_type": type_id, "role": role_id, "site": site_id},
            headers=self._headers,
        )
        self._handle_response(r)
        return r.json()

    def delete_device(self, device_id: int):
        """
        Deletes a device from NetBox.
        """
        r = httpx.delete(
            f"{self._base_url}/dcim/devices/{device_id}/",
            headers=self._headers,
        )
        self._handle_response(r)

    def create_zone(self, name: str):
        """
        Creates a new zone in NetBox.
        """
        r = httpx.post(
            f"{self._base_url}/dcim/sites/",
            json={
                "name": name,
                "slug": slugify(name),
                "region": settings.NETBOX_DEFAULT_SITE_REGION,
                "group": settings.NETBOX_DEFAULT_SITE_GROUP,
            },
            headers=self._headers,
        )
        self._handle_response(r)
        return r.json()

    def _handle_response(self, response):
        """
        Handles HTTP response, raising exceptions for unexpected status codes.
        """
        if response.status_code not in [201, 204]:
            raise HTTPException(status_code=response.status_code, detail=response.json())
