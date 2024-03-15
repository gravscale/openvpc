from fastapi import status


def test_post_router_should_return_201(create_router):
    response = create_router
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None


def test_get_router_should_return_200(client, create_router):
    router_id = create_router.json().get("id")
    response = client.get(f"/router/{router_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == router_id


def test_delete_router_should_return_204(client, create_router):
    router_id = create_router.json().get("id")
    response = client.delete(f"/router/{router_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
