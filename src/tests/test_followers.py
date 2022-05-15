from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_user_tags(async_client: AsyncClient):
    response = await async_client.get(
        '/followers/user_tags?username=Adam_Skorupa&limit=10&offset=0'
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['user_tags']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['user_tags'][0]['tag_id'] == 1
    assert response['user_tags'][0]['tag_name'] == 'Wakacje 2022'
    assert response['user_tags'][1]['tag_id'] == 2
    assert response['user_tags'][1]['tag_name'] == 'Wakacje Grecja'


@mark.asyncio
async def test_get_user_tag_without_existing_username(async_client: AsyncClient):
    response = await async_client.get(
        '/followers/user_tags?username=definitely_not_user&limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User not found'


@mark.asyncio
async def test_get_user_tag_alcohols(
        async_client: AsyncClient,
):
    response = await async_client.get(
        '/followers/user_tags/alcohols/3?limit=10&offset=0'
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 1
    assert response['alcohols'][0]['alcohol_id'] == 1
    assert response['alcohols'][0]['name'] == 'Żywiec białe'
    assert response['alcohols'][0]['kind'] == 'piwo'
    assert response['alcohols'][0]['type'] == 'witbier'
    assert response['alcohols'][0]['image_name'] == 'zywiec_biale'
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 1


@mark.asyncio
async def test_get_user_tag_alcohols_without_existing_tag_id(async_client: AsyncClient):
    response = await async_client.get(
        '/followers/user_tags/alcohols/10?limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'
