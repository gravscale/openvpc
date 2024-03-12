import pytest
from faker import Faker
from fastapi import status

fake = Faker()


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
    return client.post("/admin/device/", json=post_device_fake_dict)


def test_router_post_device_should_return_201(create_device):
    assert create_device.status_code == status.HTTP_201_CREATED


def test_router_delete_device_should_return_204(client, create_device):
    response = client.delete(f"/admin/device/{create_device.json()['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
