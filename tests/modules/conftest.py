import pytest
from faker import Faker
from fastapi import status

from app.services.netbox_service import NetboxService
from app.services.vyos import DeviceVyos

fake = Faker("pt_BR")


@pytest.fixture
def response_create_device():
    return {
        "id": fake.random_int(),
        "url": "http://netbox.gravmanage.com/api/dcim/devices/1/",
        "display": fake.name(),
        "name": fake.name(),
        "device_type": {
            "id": fake.random_int(),
            "url": "http://netbox.gravmanage.com/api/dcim/device-types/1/",
            "display": "R740",
            "manufacturer": {
                "id": fake.random_int(),
                "url": "http://netbox.gravmanage.com/api/dcim/manufacturers/1/",
                "display": "Dell",
                "name": "Dell",
                "slug": "dell",
            },
            "model": "R740",
            "slug": "r740",
        },
        "role": {
            "id": fake.random_int(),
            "url": "http://netbox.gravmanage.com/api/dcim/device-roles/1/",
            "display": "VPC",
            "name": "VPC",
            "slug": "vpc",
        },
        "device_role": {
            "id": fake.random_int(),
            "url": "http://netbox.gravmanage.com/api/dcim/device-roles/1/",
            "display": "VPC",
            "name": "VPC",
            "slug": "vpc",
        },
        "tenant": None,
        "platform": None,
        "serial": "",
        "asset_tag": None,
        "site": {
            "id": fake.random_int(),
            "url": "http://netbox.gravmanage.com/api/dcim/sites/1/",
            "display": "Under SP1",
            "name": "Under SP1",
            "slug": "under-sp1",
        },
        "location": None,
        "rack": None,
        "position": None,
        "face": None,
        "latitude": None,
        "longitude": None,
        "parent_device": None,
        "status": {"value": "active", "label": "Active"},
        "airflow": {"value": "front-to-rear", "label": "Front to rear"},
        "primary_ip": None,
        "primary_ip4": None,
        "primary_ip6": None,
        "oob_ip": None,
        "cluster": None,
        "virtual_chassis": None,
        "vc_position": None,
        "vc_priority": None,
        "description": "",
        "comments": "",
        "config_template": None,
        "config_context": {},
        "local_context_data": None,
        "tags": [],
        "custom_fields": {"operationalsystem": None},
        "created": "2024-03-04T20:56:42.007432Z",
        "last_updated": "2024-03-04T20:56:42.007507Z",
        "console_port_count": 0,
        "console_server_port_count": 0,
        "power_port_count": 0,
        "power_outlet_count": 0,
        "interface_count": 0,
        "front_port_count": 0,
        "rear_port_count": 0,
        "device_bay_count": 0,
        "module_bay_count": 0,
        "inventory_item_count": 0,
    }


@pytest.fixture
def register_credential_db(client):
    response = client.post(
        url="/admin/credential/",
        json={
            "name": fake.name(),
            "username": fake.user_name(),
            "password": fake.password(),
        },
    )
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def register_zone_db(client):
    response = client.post(url="/admin/zone/", json={"name": fake.name()})
    assert response.status_code == status.HTTP_201_CREATED
    return response.json()


@pytest.fixture
def post_device_fake_dict(register_credential_db, register_zone_db):
    return {
        "name": fake.name(),
        "device_type": "vyos",
        "host": fake.ipv4_private(),
        "port": 8080,
        "protocol": "https",
        "credential_id": register_credential_db["id"],
        "zone_id": register_zone_db["id"],
    }


@pytest.fixture
def mock_monkey_patch(monkeypatch, response_create_device):
    async def mock_create_device(*args, **kwargs):
        return response_create_device

    monkeypatch.setattr(NetboxService, "create_device", mock_create_device)
    monkeypatch.setattr(NetboxService, "delete_device", None)
    monkeypatch.setattr(DeviceVyos, "is_connected", True)
