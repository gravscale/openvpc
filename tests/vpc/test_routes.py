from fastapi import status


def test_vpc(client, create_vpc):
    response = create_vpc

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None

    vpc_id = response.json().get("id")
    response = client.get(f"/vpc/{vpc_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == vpc_id
