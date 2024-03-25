from fastapi import status


def test_device(client, create_device):
    response = create_device

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None

    device_id = response.json().get("id")
    response = client.get(f"/admin/device/{device_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == device_id

    device_id = response.json().get("id")
    response = client.delete(f"/admin/device/{device_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
