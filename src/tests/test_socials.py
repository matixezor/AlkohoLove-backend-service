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
    response = await async_client.get('socials/users?phrase=Dar', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == USERS_FIXTURE


@mark.asyncio
async def test_search_users_by_phrase_case_insensitive(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/users?phrase=dar', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == USERS_FIXTURE


@mark.asyncio
async def test_search_users_by_phrase_no_current_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/users?phrase=Adam', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 0
    assert response['page_info']['total'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == []


@mark.asyncio
async def test_get_user_info(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/user_info/6288e2fdd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == '6288e2fdd5ab6070dde8db8c'
    assert response['username'] == 'Adam_Skorupa'
    assert response['created_on'] == "2022-04-12T06:11:15+00:00"
    assert response['rate_count'] == 2
    assert response['avg_rating'] == 5
    assert response['followers_count'] == 0
    assert response['following_count'] == 0
    assert response['favourites_count'] == 0


@mark.asyncio
async def test_get_user_info_that_not_exists(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('socials/user_info/6288e2fdd5ab6070dde8db8f', headers=user_token_headers)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Nie znaleziono użytkownika.'
