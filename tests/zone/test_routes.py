from fastapi import status


def test_zone(client, create_zone):
    response = create_zone

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None

    zone_id = response.json().get("id")
    response = client.get(f"/admin/zone/{zone_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == zone_id
