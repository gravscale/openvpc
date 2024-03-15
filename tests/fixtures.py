from dataclasses import dataclass

import pytest
from faker import Faker

from src.core.device_vyos import DeviceVyos
from src.core.netbox_service import NetboxService

fake = Faker()  # "pt_BR"


@pytest.fixture
def create_zone(client):
    data = {"name": fake.name()}
    return client.post("/admin/zone/", json=data)


@pytest.fixture
def create_credential(client):
    data = {
        "name": fake.name(),
        "username": fake.user_name(),
        "password": fake.password(),
    }
    return client.post("/admin/credential/", json=data)


@pytest.fixture
def create_device(client, create_credential, create_zone, mock_monkeypatch):
    data = {
        "name": fake.name(),
        "device_type": "vyos",
        "host": fake.ipv4_private(),
        "port": 8080,
        "protocol": "https",
        "credential_id": create_credential.json().get("id"),
        "zone_id": create_zone.json().get("id"),
    }
    return client.post("/admin/device/", json=data)


@pytest.fixture
def create_config(client, create_zone):
    data = {
        "param": fake.word(),
        "value": fake.word(),
        "format": "string",
        "scope_zone_id": create_zone.json().get("id"),
    }
    return client.post("/admin/configuration/", json=data)


@pytest.fixture
def create_vpc(client):
    data = {
        "name": fake.name(),
        "device_name_primary": fake.name(),
        "device_name_secondary": fake.name(),
    }
    return client.post("/vpc/", json=data)


@pytest.fixture
def create_router(client, create_vpc):
    data = {
        "name": fake.name(),
        "vpc_id": create_vpc.json().get("id"),
    }
    return client.post("/router/", json=data)


@pytest.fixture
def response_pyvyos_device_show():
    @dataclass
    class ApiResponse:
        error: str

    return ApiResponse(error=False)


@pytest.fixture
def mock_monkeypatch(monkeypatch, response_pyvyos_device_show):
    def mock_netbox_create(*args, **kwargs):
        return {"id": fake.random_int()}

    def mock_netbox_delete(*args, **kwargs):
        return None

    def mock_pyvyos_device_show(*args, **kwargs):
        return response_pyvyos_device_show

    monkeypatch.setattr(NetboxService, "create_device", mock_netbox_create)
    monkeypatch.setattr(NetboxService, "create_zone", mock_netbox_create)
    monkeypatch.setattr(NetboxService, "delete_device", mock_netbox_delete)
    monkeypatch.setattr(DeviceVyos, "show", mock_pyvyos_device_show)
