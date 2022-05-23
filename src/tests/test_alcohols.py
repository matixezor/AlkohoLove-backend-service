from pytest import mark
from httpx import AsyncClient


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
    'avg_rating': 0.0,
    'rate_count': 0,
    'rate_value': 0,
    'age': 4
}


@mark.asyncio
async def test_search_alcohols(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
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
