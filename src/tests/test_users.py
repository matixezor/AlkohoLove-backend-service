from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_users_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/users', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_user_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/users/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_update_user_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.put(
        '/users/1', headers={'Authorization': f'Bearer {user_token}'}, json={'username': 'test'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_user(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/users/3', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['user_id'] == 3
    assert response['username'] == 'DariuszGołąbski'
    assert response['email'] == 'dariusz.golabski@gmail.com'
    assert response['last_login'] == '2022-04-21T12:32:43'
    assert response['created_on'] == '2022-01-08T08:16:42'
    assert response['is_banned'] is False


@mark.asyncio
async def test_get_users(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/users?limit=1&offset=2', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 3
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 2
    assert response['users'][0]['username'] == 'DariuszGołąbski'
    assert response['users'][0]['email'] == 'dariusz.golabski@gmail.com'
    assert response['users'][0]['last_login'] == '2022-04-21T12:32:43'
    assert response['users'][0]['created_on'] == '2022-01-08T08:16:42'
    assert response['users'][0]['is_banned'] is False


@mark.asyncio
async def test_get_user_tags(async_client: AsyncClient):
    response = await async_client.get(
        '/users/tags/DariuszGołąbski?limit=10&offset=0'
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['user_tags']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['user_tags'][0]['tag_id'] == 3
    assert response['user_tags'][0]['tag_name'] == 'Alkohole do grilla'
    assert response['user_tags'][1]['tag_id'] == 4
    assert response['user_tags'][1]['tag_name'] == 'Grill u Huberta'


@mark.asyncio
async def test_get_user_tag_without_existing_username(async_client: AsyncClient):
    response = await async_client.get(
        '/users/tags/definitely_not_user?limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User not found'


@mark.asyncio
async def test_get_user_tag_alcohols(
        async_client: AsyncClient,
):
    response = await async_client.get(
        '/users/tags/3/alcohols?limit=10&offset=0'
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 1
    assert response['alcohols'][0]['alcohol_id'] == 1
    assert response['alcohols'][0]['name'] == 'Żywiec białe'
    assert response['alcohols'][0]['kind'] == 'piwo'
    assert response['alcohols'][0]['type'] == 'witbier'
    assert response['alcohols'][0]['alcohol_by_volume'] == 4.9
    assert response['alcohols'][0]['manufacturer'] == 'Żywiec'
    assert response['alcohols'][0]['rating'] == 5
    assert response['alcohols'][0]['image_name'] == 'zywiec_biale'
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 1


@mark.asyncio
async def test_get_user_tag_alcohols_without_existing_tag_id(async_client: AsyncClient):
    response = await async_client.get(
        '/users/tags/10/alcohols?limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'
