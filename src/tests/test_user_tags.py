from pytest import mark
from httpx import AsyncClient

PAYLOAD_FIXTURE = {
        "tag_name": "test_tag",
        "user_id": 3,
        "alcohol_ids": [1]
    }


@mark.asyncio
async def test_create_user_tag(async_client: AsyncClient):
    data = {
        "tag_name": "test_tag",
        "user_id": 3,
        "alcohol_ids": [1]
    }
    response = await async_client.post('/user_tags', json=data)
    assert response.status_code == 201


@mark.asyncio
async def test_create_user_tag_with_existing_name_and_user_id(async_client: AsyncClient):
    data = {
        "tag_name": "Alkohole do grilla",
        "user_id": 3,
        "alcohol_ids": [2]
    }
    response = await async_client.post('/user_tags', json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag with given name and user id already exists'


@mark.asyncio
async def test_create_user_tag_without_required_data(async_client: AsyncClient):
    response = await async_client.post('/user_tags')
    assert response.status_code == 422


@mark.asyncio
async def test_get_user_tags(async_client: AsyncClient):
    response = await async_client.get(
        '/user_tags/1?limit=10&offset=0'
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
async def test_get_user_tags_with_not_existing_tag_id(async_client: AsyncClient):
    response = await async_client.get(
        '/user_tags/alcohols/10?limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'


@mark.asyncio
async def test_add_alcohol_to_user_tag(async_client: AsyncClient):
    response = await async_client.post(
        '/user_tags/alcohols/3?alcohol_id=2'
    )
    assert response.status_code == 201


@mark.asyncio
async def test_add_alcohol_to_user_tag_with_existing_alcohol_in_user_tag(async_client: AsyncClient):
    response = await async_client.post(
        '/user_tags/alcohols/1?alcohol_id=1'
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol already exists in user tag'


@mark.asyncio
async def test_add_alcohol_to_user_tag_without_existing_user_tag(async_client: AsyncClient):
    response = await async_client.post(
        '/user_tags/alcohols/13?alcohol_id=1'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'


@mark.asyncio
async def test_add_alcohol_to_user_tag_without_existing_alcohol(async_client: AsyncClient):
    response = await async_client.post(
        '/user_tags/alcohols/1?alcohol_id=13'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Alcohol not found'


@mark.asyncio
async def test_delete_user_tag(async_client: AsyncClient):
    response = await async_client.delete('/user_tags/1')
    assert response.status_code == 204


@mark.asyncio
async def test_delete_alcohol_from_user_tag(async_client: AsyncClient):
    response = await async_client.delete('/user_tags/alcohol/1?alcohol_id=1')
    assert response.status_code == 204


@mark.asyncio
async def test_update_user_tag(async_client: AsyncClient):
    data = {
        "user_id": 1,
        "tag_name": "test_name"
    }
    response = await async_client.put('/user_tags/2', json=data)
    assert response.status_code == 200
    response = response.json()
    assert response['tag_id'] == 2
    assert response['tag_name'] == 'test_name'


@mark.asyncio
async def test_update_user_tag_without_existing_tag_id(async_client: AsyncClient):
    data = {
        "user_id": 1,
        "tag_name": "test_name",
    }
    response = await async_client.put('/user_tags/100', json=data)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'


@mark.asyncio
async def test_update_user_tag_without_required_data(async_client: AsyncClient):
    response = await async_client.put('/user_tags/2')
    assert response.status_code == 422


@mark.asyncio
async def test_update_user_tag_with_existing_name(async_client: AsyncClient):
    data = {
        "user_id": 3,
        "tag_name": "Grill u Huberta",
    }
    response = await async_client.put('/user_tags/3', json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag with given name and user id already exists'
