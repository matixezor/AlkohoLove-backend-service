from pytest import mark
from httpx import AsyncClient

from src.tests.response_fixtures.followers_fixtures import FOLLOWERS_FIXTURE, FOLLOWING_FIXTURE, USERS_FIXTURE


@mark.asyncio
async def test_get_followers(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/followers/6288e2fdd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == FOLLOWERS_FIXTURE


@mark.asyncio
async def test_get_following(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/following/6288e2fdd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == FOLLOWING_FIXTURE


@mark.asyncio
async def test_search_users_by_phrase(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/users?phrase=Ada', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == USERS_FIXTURE
