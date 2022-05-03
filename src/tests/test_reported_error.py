from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_reported_error(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/reported_error/1', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['error_id'] == 1
    assert response['description'] == 'Test error description'
    assert response['user_id'] == 1


@mark.asyncio
async def test_get_reported_errors(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/reported_error?limit=1&offset=0', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reported_error']) == 1
    assert response['page_info']['total'] == 3
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['reported_errors'][0]['error_id'] == 1
    assert response['reported_errors'][0]['description'] == 'Test error description'
    assert response['reported_errors'][0]['user'][0] == 'admin'
    assert response['reported_errors'][0]['user'][1] == 'admin@gmail.com'
