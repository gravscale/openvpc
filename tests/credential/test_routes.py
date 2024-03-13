from fastapi import status


def test_post_credential_should_return_201(create_credential):
    assert create_credential.status_code == status.HTTP_201_CREATED


def test_delete_credential_should_return_204(client, create_credential):
    credential_id = create_credential.json()["id"]
    response = client.delete(url=f"/admin/credential/{credential_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
