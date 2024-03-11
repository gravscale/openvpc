from fastapi import status

ENDPOINT = "/admin/device"


def test_router_post_device_should_return_201(create_device):
    assert create_device.status_code == status.HTTP_201_CREATED


def test_router_delete_device_should_return_204(client, create_device):
    response = client.delete(url=f"{ENDPOINT}/{create_device.json()['id']}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
