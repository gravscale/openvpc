from fastapi import status


def test_router_post_credential_should_return_201(create_credential):
    assert create_credential.status_code == status.HTTP_201_CREATED


def test_router_delete_credential_should_return_204(client, create_credential):
    response = client.delete(url=f"/admin/credential/{create_credential.json()["id"]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
