from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_post_reported_error(async_client: AsyncClient, user_token_headers):
    data = {
        'description': 'test',
        'user_id': 2
    }
    response = await async_client.post('/reported_errors', json=data, headers=user_token_headers)
    assert response.status_code == 201
