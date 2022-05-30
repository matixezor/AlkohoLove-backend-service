from pytest import mark
from httpx import AsyncClient

from src.tests.response_fixtures.list_fixtures import WISHLIST_FIXTURE, FAVOURITES_FIXTURE, SEARCH_HISTORY_FIXTURE


@mark.asyncio
async def test_get_wishlist(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/list/wishlist/6288e2fdd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'] == WISHLIST_FIXTURE


@mark.asyncio
async def test_get_favourites(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/list/favourites/6288e2fdd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'] == FAVOURITES_FIXTURE


@mark.asyncio
async def test_get_search_history(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/list/search_history/6288e2fdd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'] == SEARCH_HISTORY_FIXTURE
