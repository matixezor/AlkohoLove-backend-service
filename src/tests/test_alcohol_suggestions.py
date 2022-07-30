from pytest import mark
from httpx import AsyncClient

from src.tests.response_fixtures.alcohol_suggestions import SUGGESTION_POST_FIXTURE, \
    SUGGESTION_SAME_USER_FIXTURE, SUGGESTION_POST_BARCODE_EXISTS_FIXTURE, SUGGESTION_POST_FIXTURE_NO_DESC


@mark.asyncio
async def test_create_suggestion(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/suggestions', headers=user_token_headers, json=SUGGESTION_POST_FIXTURE)
    assert response.status_code == 201


@mark.asyncio
async def test_create_suggestion_without_data(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/suggestions', headers=user_token_headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_suggestion_same_barcode_same_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/suggestions', headers=user_token_headers,
                                       json=SUGGESTION_SAME_USER_FIXTURE)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User already made a suggestion for this alcohol'


@mark.asyncio
async def test_create_suggestion_when_barcode_exists(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/suggestions', headers=user_token_headers,
                                       json=SUGGESTION_POST_BARCODE_EXISTS_FIXTURE)
    assert response.status_code == 201


@mark.asyncio
async def test_create_suggestion_with_no_description(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/suggestions', headers=user_token_headers, json=SUGGESTION_POST_FIXTURE_NO_DESC)
    assert response.status_code == 201
