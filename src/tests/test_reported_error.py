from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_reported_error_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/reported_error', headers={'Authorization': f'Bearer {user_token}'}
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
        '/users?limit=1&offset=0', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 3
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['users'][0]['username'] == 'DariuszGołąbski'
    assert response['users'][0]['email'] == 'dariusz.golabski@gmail.com'
    assert response['users'][0]['last_login'] == '2022-04-21T12:32:43'
    assert response['users'][0]['created_on'] == '2022-01-08T08:16:42'
    assert response['users'][0]['is_banned'] is False
