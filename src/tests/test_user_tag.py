from pytest import mark
from httpx import AsyncClient

TAG_ALCOHOLS_FIXTURE = [
    {
        'name': 'Jameson',
        'kind': 'whisky',
        'type': 'blended',
        'alcohol_by_volume': 40.0,
        'description': 'Lorem ipsum',
        'color': 'bursztyn',
        'manufacturer': 'Irish Distillers',
        'country': 'Irlandia',
        'region': 'Cork',
        'food': ['czekoladowy mus'],
        'finish': ['gładki', 'słodki', 'pikantny'],
        'aroma': ['kwiaty', 'owoce', 'nuty korzenne', 'drewno'],
        'taste': ['nuty korzenne', 'orzechy', 'wanilia', 'słodkie sherry', 'łagodny'],
        'barcode': ['5011007003234', '5011007015534', '5011007003005'],
        'keywords': ['czteroletnia', 'irlandzka', 'irlandzkie', 'blend'],
        'id': '6288e32dd5ab6070dde8db8a',
        'avg_rating': 0.0,
        'rate_count': 0,
        'rate_value': 0,
        'age': 4
    },
    {
        "id": '6288e32dd5ab6070dde8db8c',
        "barcode": ['7312040017072'],
        "kind": 'wódka',
        "name": 'Absolut Vodka',
        "type": 'czysta',
        "description": 'Lorem ipsum',
        "alcohol_by_volume": 40.0,
        "color": 'bezbarwny',
        "country": 'Szwecja',
        "region": 'Ahus',
        "manufacturer": 'The Absolut Company',
        "food": [],
        "taste": [],
        "aroma": [],
        "finish": [],
        "rate_count": 0,
        "rate_value": 0,
        "avg_rating": 0.0,
        "keywords": ['szwedzka']
    }

]


@mark.asyncio
async def test_create_tag(async_client: AsyncClient, user_token_headers: dict[str, str]):
    data = {
        'tag_name': 'test'
    }
    response = await async_client.post('/me/tags', json=data, headers=user_token_headers)
    assert response.status_code == 201


@mark.asyncio
async def test_create_tag_with_existing_name(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        'tag_name': 'grill u huberta'
    }
    response = await async_client.post('/me/tags', json=data, headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Tag already exists'


@mark.asyncio
async def test_create_tag_without_required_data(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/tags', headers=user_token_headers)
    assert response.status_code == 422


@mark.asyncio
async def test_get_tags(async_client: AsyncClient, user_token_headers: dict[str, str]):

    response = await async_client.get('/me/tags?limit=10&offset=0', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['user_tags']) == 2
    assert response['user_tags'][0]['tag_name'] == 'grill u huberta'
    assert response['user_tags'][0]['id'] == '628f9071f32df3b39ced1a3a'
    assert response['user_tags'][1]['tag_name'] == 'wakacje 2021'
    assert response['user_tags'][1]['id'] == '628f9071f32df3b39ced1a3b'
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2


@mark.asyncio
async def test_get_alcohols_with_not_existing_tag(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/me/tags/628f9071f32df3b39ced1a3d/alcohols?limit=10&offset=0', headers=user_token_headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Tag not found'


@mark.asyncio
async def test_get_alcohols(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/me/tags/628f9071f32df3b39ced1a3b/alcohols?limit=10&offset=0', headers=user_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2
    assert response['alcohols'] == TAG_ALCOHOLS_FIXTURE


@mark.asyncio
async def test_add_alcohol(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/tags/628f9071f32df3b39ced1a3a/alcohol/6288e32dd5ab6070dde8db8b',
        headers=user_token_headers
    )
    assert response.status_code == 201


@mark.asyncio
async def test_add_alcohol_with_existing_alcohol_in_tag(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/tags/628f9071f32df3b39ced1a3a/alcohol/6288e32dd5ab6070dde8db8a',
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol already is in tag'


@mark.asyncio
async def test_add_alcohol_without_existing_tag(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/tags/628f9071f32df3b39ced1a3d/alcohol/6288e32dd5ab6070dde8db8a',
        headers=user_token_headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Tag not found'


@mark.asyncio
async def test_add_alcohol_without_existing_alcohol(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/tags/628f9071f32df3b39ced1a3a/alcohol/6288e32dd5ab6070dde8db9a',
        headers=user_token_headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Alcohol not found'


@mark.asyncio
async def test_add_alcohol_to_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/tags/628f9071f32df3b39ced1a3c/alcohol/6288e32dd5ab6070dde8db8a',
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Tag does not belong to user'


@mark.asyncio
async def test_delete_tag(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/me/tags/628f9071f32df3b39ced1a3a',
        headers=user_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_delete_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/me/tags/628f9071f32df3b39ced1a3c',
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Tag does not belong to user'


@mark.asyncio
async def test_remove_alcohol_from_tag(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/me/tags/628f9071f32df3b39ced1a3a/alcohol/6288e32dd5ab6070dde8db8a',
        headers=user_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_remove_alcohol_from_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/me/tags/628f9071f32df3b39ced1a3c/alcohol/6288e32dd5ab6070dde8db8a',
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Tag does not belong to user'


@mark.asyncio
async def test_update_tag(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put(
        '/me/tags/628f9071f32df3b39ced1a3a?tag_name=test',
        headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['tag_name'] == 'test'
    assert response['_id'] == '628f9071f32df3b39ced1a3a'


@mark.asyncio
async def test_update_tag_that_not_exists(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put(
        '/me/tags/628f9071f32df3b39ced1a3d?tag_name=test',
        headers=user_token_headers)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Tag not found'


@mark.asyncio
async def test_update_tag_with_existing_name(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put(
        '/me/tags/628f9071f32df3b39ced1a3a?tag_name=grill u huberta',
        headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Tag already exists'


@mark.asyncio
async def test_update_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put(
        '/me/tags/628f9071f32df3b39ced1a3c?tag_name=test',
        headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Tag does not belong to user'
