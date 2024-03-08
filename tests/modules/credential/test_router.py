from fastapi import status

ENDPOINT = "/admin/credential"


def test_router_post_credential_should_return_201(register_credential_db):
    pass


def test_router_delete_credential_should_return_204(client, register_credential_db):
    response = client.delete(url=f"{ENDPOINT}/{register_credential_db["id"]}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
