from fastapi import status


def test_credential(client, create_credential):
    resp = create_credential

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp.json().get("id") is not None

    credential_id = resp.json().get("id")
    resp = client.get(f"/admin/credential/{credential_id}")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json().get("id") == credential_id

    resp = client.delete(f"/admin/credential/{credential_id}")

    assert resp.status_code == status.HTTP_204_NO_CONTENT
