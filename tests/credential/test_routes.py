from fastapi import status


def test_post_credential_should_return_201(create_credential):
    response = create_credential
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None


def test_get_credential_should_return_200(client, create_credential):
    credential_id = create_credential.json().get("id")
    response = client.get(f"/admin/credential/{credential_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("id") == credential_id


def test_delete_credential_should_return_204(client, create_credential):
    credential_id = create_credential.json().get("id")
    response = client.delete(f"/admin/credential/{credential_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
