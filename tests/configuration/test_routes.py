from fastapi import status


def test_post_config_should_return_201(client, create_config):
    assert create_config.status_code == status.HTTP_201_CREATED
