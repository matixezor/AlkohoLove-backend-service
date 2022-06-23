from pytest import mark
from httpx import AsyncClient

from src.tests.response_fixtures.alcohol_filters_fixtures import ALCOHOL_FILTER_FIXTURE

ALCOHOL_FIXTURE = {
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
    'avg_rating': 5.0,
    'rate_count': 1,
    'rate_value': 5,
    'age': 4
}

ALCOHOL_CATEGORY_FIXTURE = {
    'id': '628d20d87bde3e0dcb2ed69b',
    'properties': {
        'kind': {
            'enum': ['piwo']
        },
        'ibu': {
            'bsonType': ['int', 'null'],
            'description': '4'
        },
        'srm': {
            'bsonType': ['double', 'null'],
            'description': '4'
        },
        'extract': {
            'bsonType': ['double', 'null'],
            'description': '11.6'
        },
        'fermentation': {
            'bsonType': ['string'],
            'description': 'górna'
        },
        'is_filtered': {
            'bsonType': ['bool'],
            'description': 'true'
        },
        'is_pasteurized': {
            'bsonType': ['bool'],
            'description': 'true'
        }
    },
    'required': ['ibu', 'srm', 'extract', 'fermentation', 'is_filtered', 'is_pasteurized'],
    'title': 'piwo'
}


@mark.asyncio
async def test_search_alcohols(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/alcohols?limit=1&offset=0', headers=user_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 1
    assert response['page_info']['total'] == 5
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['alcohols'][0] == ALCOHOL_FIXTURE


@mark.asyncio
async def search_alcohols_with_filters_with_empty_kind(async_client: AsyncClient):
    body = {'kind': ''}
    response = await async_client.post(
        '/alcohols?limit=1&offset=0', json=body
    )
    assert response.status_code == 422
    response = response.json()
    assert response['detail'] == 'Kind filter must be provided'


@mark.asyncio
async def search_alcohols_with_filters_without_kind(async_client: AsyncClient):
    body = {'color': ['test']}
    response = await async_client.post(
        '/alcohols?limit=1&offset=0', json=body
    )
    assert response.status_code == 422


@mark.asyncio
async def test_get_alcohol_by_barcode(async_client: AsyncClient):
    response = await async_client.get('/alcohols/5011007003234')
    assert response.status_code == 200
    assert response.json() == ALCOHOL_FIXTURE


@mark.asyncio
async def test_get_alcohol_by_non_existing_barcode(async_client: AsyncClient):
    response = await async_client.get('/alcohols/5900699104827')
    assert response.status_code == 404
    assert response.json() == {
        'detail': 'Alcohol not found'
    }


@mark.asyncio
async def test_get_alcohol_filters(async_client: AsyncClient):
    response = await async_client.get('/alcohols/filters')
    assert response.status_code == 200
    response = response.json()
    assert len(response['filters']) == 4
    assert response['filters'][0] == ALCOHOL_FILTER_FIXTURE


@mark.asyncio
async def test_get_schemas(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get('/alcohols/metadata/categories', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['page_info']['total'] == 7
    assert response['categories'][1]['id'] == ALCOHOL_CATEGORY_FIXTURE['id']
    assert response['categories'][1]['title'] == ALCOHOL_CATEGORY_FIXTURE['title']
    assert response['categories'][1]['required'] == ALCOHOL_CATEGORY_FIXTURE['required']
    assert response['categories'][1]['properties'] == [
        {'name': 'kind', 'metadata': {'enum': ['piwo']}},
        {'name': 'ibu', 'metadata': {'title': 'ibu', 'bsonType': ['int', 'null'], 'description': '4'}},
        {'name': 'srm', 'metadata': {'title': 'srm', 'bsonType': ['double', 'null'], 'description': '4'}},
        {'name': 'extract', 'metadata': {'title': 'ekstrakt', 'bsonType': ['double', 'null'], 'description': '11.6'}},
        {'name': 'fermentation', 'metadata': {'title': 'fermentacja', 'bsonType': ['string'], 'description': 'górna'}},
        {'name': 'is_filtered', 'metadata': {'title': 'filtrowane', 'bsonType': ['bool'], 'description': 'true'}},
        {'name': 'is_pasteurized', 'metadata': {'title': 'pasteryzowane', 'bsonType': ['bool'], 'description': 'true'}}
    ]
