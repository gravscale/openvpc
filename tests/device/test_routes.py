from fastapi import status


def test_post_device_should_return_201(create_device):
    response = create_device
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None


def test_get_device_should_return_200(client, create_device):
    device_id = create_device.json().get("id")
    response = client.get(f"/admin/device/{device_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == device_id


def test_delete_device_should_return_204(client, create_device, mock_monkeypatch):
    device_id = create_device.json().get("id")
    response = client.delete(f"/admin/device/{device_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
