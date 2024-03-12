from fastapi import status


def test_router_post_zone_should_return_201(create_zone):
    assert create_zone.status_code == status.HTTP_201_CREATED
