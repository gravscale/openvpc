from fastapi import status


def test_router(client, create_router):
    response = create_router

    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None

    router_id = response.json().get("id")
    response = client.get(f"/router/{router_id}")

    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == router_id

    router_id = response.json().get("id")
    response = client.delete(f"/router/{router_id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
