import pytest
from faker import Faker
from fastapi import status

fake = Faker()


@pytest.fixture
def post_config_fake_dict(create_zone):
    return {
        "param": fake.word(),
        "value": fake.word(),
        "format": "string",
        "scope_zone_id": create_zone.json()["id"],
    }


def test_router_post_config_should_return_201(client, post_config_fake_dict):
    r = client.post("/admin/configuration/", json=post_config_fake_dict)
    assert r.status_code == status.HTTP_201_CREATED
