from fastapi import status


def test_post_vpc_should_return_201(create_vpc):
    response = create_vpc
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None


def test_get_vpc_should_return_200(client, create_vpc):
    vpc_id = create_vpc.json().get("id")
    response = client.get(f"/vpc/{vpc_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == vpc_id
