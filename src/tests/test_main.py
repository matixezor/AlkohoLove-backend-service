from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_root(async_client: AsyncClient):
    response = await async_client.get('/')
    assert response.status_code == 200
