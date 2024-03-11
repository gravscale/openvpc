from dataclasses import dataclass

import pytest
from faker import Faker

from app.core.device_vyos import DeviceVyos
from app.core.netbox_service import NetboxService

fake = Faker("pt_BR")


@pytest.fixture
def create_credential(client):
    return client.post(
        url="/admin/credential/",
        json={"name": fake.name(), "username": fake.user_name(), "password": fake.password()},
    )


@pytest.fixture
def create_zone(client):
    return client.post(url="/admin/zone/", json={"name": fake.name()})


@pytest.fixture
def post_device_fake_dict(create_credential, create_zone):
    return {
        "name": fake.name(),
        "device_type": "vyos",
        "host": fake.ipv4_private(),
        "port": 8080,
        "protocol": "https",
        "credential_id": create_credential.json()["id"],
        "zone_id": create_zone.json()["id"],
    }


@pytest.fixture
def create_device(client, post_device_fake_dict, mock_monkey_patch):
    return client.post(url="/admin/device/", json=post_device_fake_dict)


@pytest.fixture
def response_netbox_create():
    return {"id": fake.random_int()}


@pytest.fixture
def response_pyvyos_device_show():
    @dataclass
    class ApiResponse:
        error: str

    return ApiResponse(error=False)


@pytest.fixture
def mock_monkey_patch(monkeypatch, response_netbox_create, response_pyvyos_device_show):
    def mock_netbox_create(*args, **kwargs):
        return response_netbox_create

    def mock_netbox_delete(*args, **kwargs):
        return None

    def mock_pyvyos_device_show(*args, **kwargs):
        return response_pyvyos_device_show

    monkeypatch.setattr(NetboxService, "create_device", mock_netbox_create)
    monkeypatch.setattr(NetboxService, "create_zone", mock_netbox_create)
    monkeypatch.setattr(NetboxService, "delete_device", mock_netbox_delete)
    monkeypatch.setattr(DeviceVyos, "show", mock_pyvyos_device_show)
