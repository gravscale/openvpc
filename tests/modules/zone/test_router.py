# from fastapi import status

ENDPOINT = "/admin/zone"


def test_router_post_zone_should_return_201(register_zone_db):
    pass


# def test_router_delete_zone_should_return_204(client, register_zone_db):
#     response = client.delete(url=f"{ENDPOINT}/{register_zone_db['id']}")
#     assert response.status_code == status.HTTP_204_NO_CONTENT