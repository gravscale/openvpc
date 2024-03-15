from fastapi import status


def test_post_config_should_return_201(create_config):
    response = create_config
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json().get("id") is not None


def test_get_config_should_return_200(client, create_config):
    config_param = create_config.json().get("param")
    response = client.get(f"/admin/configuration/{config_param}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json().get("param") == config_param
