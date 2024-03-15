from fastapi import status


def test_post_zone_should_return_201(create_zone):
    response = create_zone
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None


def test_get_zone_should_return_200(client, create_zone):
    zone_id = create_zone.json().get("id")
    response = client.get(f"/admin/zone/{zone_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == zone_id
