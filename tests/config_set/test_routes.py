from fastapi import status


def test_config(client, create_config):
    resp = create_config
    resp_json = resp.json()

    assert resp.status_code == status.HTTP_201_CREATED
    assert resp_json.get("id") is not None

    param = resp_json.get("param")
    resp = client.get(f"/admin/configuration/{param}")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json().get("param") == param
