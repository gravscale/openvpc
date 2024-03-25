from dataclasses import dataclass

import pytest
from faker import Faker

fake = Faker()  # "pt_BR"


@pytest.fixture
def create_zone(client, mock_monkeypatch):
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
        "primary_device_name": fake.name(),
        "secondary_device_name": fake.name(),
    }
    return client.post("/vpc/", json=data)


@pytest.fixture
def create_router(client, create_vpc, mock_monkeypatch):
    data = {
        "name": fake.name(),
        "vpc_id": create_vpc.json().get("id"),
    }
    return client.post("/router/", json=data)


@pytest.fixture
def mock_monkeypatch(monkeypatch):
    from src.core.device_vyos import DeviceVyos
    from src.netbox.schemas import NetboxDefaultResponse
    from src.netbox.service import NetboxService

    def mock_netbox_create(*args, **kwargs):
        return NetboxDefaultResponse(id=fake.random_int())

    def mock_netbox_delete(*args, **kwargs):
        return None

    def mock_pyvyos_device_show(*args, **kwargs):
        @dataclass
        class ApiResponse:
            error: str

        return ApiResponse(error=False)

    monkeypatch.setattr(NetboxService, "create_device", mock_netbox_create)
    monkeypatch.setattr(NetboxService, "delete_device", mock_netbox_delete)
    monkeypatch.setattr(NetboxService, "create_site", mock_netbox_create)
    monkeypatch.setattr(DeviceVyos, "show", mock_pyvyos_device_show)
