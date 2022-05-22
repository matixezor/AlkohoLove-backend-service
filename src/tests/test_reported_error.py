from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_reported_error(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/reported_error/user/1', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['error_id'] == 1
    assert response['description'] == 'Test error description'
    assert response['user']['username'] == 'user'
    assert response['user']['email'] == 'user@gmail.com'


@mark.asyncio
async def test_get_reported_error_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/reported_error/user/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_reported_errors(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/reported_error/user?limit=1&offset=0', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reported_errors']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['reported_errors'][0]['error_id'] == 1
    assert response['reported_errors'][0]['description'] == 'Test error description'
    assert response['reported_errors'][0]['user']['username'] == 'user'
    assert response['reported_errors'][0]['user']['email'] == 'user@gmail.com'


@mark.asyncio
async def test_get_reported_errors_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/reported_error/user?limit=1&offset=0', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_reported_error(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/reported_error/user/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_reported_error_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.delete('/reported_error/user/1', headers=headers)
    assert response.status_code == 403


@mark.asyncio
async def test_post_reported_error(async_client: AsyncClient):
    data = {
        'description': 'test',
        'user_id': 2
    }
    response = await async_client.post('/reported_error', json=data)
    assert response.status_code == 201
