from pytest import mark
from httpx import AsyncClient

PAYLOAD_FIXTURE = {
        'barcode_list': ['12345323632'],
        'name': 'test_name',
        'kind': 'test_kind',
        'type': 'test_type',
        'alcohol_by_volume': 1,
        'manufacturer': 'test_manufacturer',
        'description': 'test_desc',
        'region_id': 1
    }


@mark.asyncio
async def test_create_alcohol_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.post(
        '/alcohols/user', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_alcohols_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/alcohols/user', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_update_alcohol_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.put(
        '/alcohols/user/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_alcohol_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.delete(
        '/alcohols/user/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_alcohol_by_barcode(async_client: AsyncClient):
    response = await async_client.get('/alcohols/5900699104827')
    assert response.status_code == 200
    response = response.json()
    assert response['alcohol_id'] == 1
    assert response['name'] == 'Żywiec białe'
    assert response['kind'] == 'piwo'
    assert response['rating'] == 5
    assert response['type'] == 'witbier'
    assert response['alcohol_by_volume'] == 4.9
    assert response['image_name'] == 'zywiec_biale'
    assert response['color'] == 'słomkowy'
    assert response['serving_temperature'] == '4-6'
    assert response['region'] == {
        'id': 1,
        'name': 'Polska',
        'country': {
            'id': 1,
            'name': 'Polska'
        }
    }
    assert response['foods'] == [{
        'id': 1,
        'name': 'białe mięso'
    }]
    assert response['aromas'] == [{
        'id': 1,
        'name': 'kolendra'
    }]
    assert response['ingredients'] == [{
        'id': 1,
        'name': 'mieszanka zbóż'
    }]
    assert response['tastes'] == []
    assert response['finishes'] == []
    assert response['bitterness_ibu'] == 18
    assert response['srm'] == 2.4
    assert response['extract'] == 11.6
    assert response['fermentation'] == "top"
    assert response['is_filtered'] is False
    assert response['is_pasteurized'] is True
    assert response['age'] is None
    assert response['year'] is None
    assert response['vine_stock'] is None
    assert response['description'] is not None


@mark.asyncio
async def test_get_alcohols(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/alcohols/user', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'][0]['alcohol_id'] == 1
    assert response['alcohols'][0]['name'] == 'Żywiec białe'


@mark.asyncio
async def test_get_alcohols_by_alcohol_name(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/alcohols/user?name=Ży', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'][0]['alcohol_id'] == 1
    assert response['alcohols'][0]['name'] == 'Żywiec białe'


@mark.asyncio
async def test_delete_alcohol(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/alcohols/user/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_create_alcohol(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/alcohols/user', headers=headers, json=PAYLOAD_FIXTURE)
    assert response.status_code == 201


@mark.asyncio
async def test_create_alcohol_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/alcohols/user', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_alcohol_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    data = PAYLOAD_FIXTURE
    data['name'] = 'Żywiec białe'
    response = await async_client.post('/alcohols/user', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol with given name already exists'


@mark.asyncio
async def test_update_alcohol_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    data = PAYLOAD_FIXTURE
    data['name'] = 'Żywiec białe'
    response = await async_client.put('/alcohols/user/2', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol with given name already exists'


@mark.asyncio
async def test_update_alcohol_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put('/alcohols/user/1', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_alcohol(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    data = {
        'year': 25,
        'food_ids': [1, 2],
        'ingredient_ids': [1]
    }
    response = await async_client.put('/alcohols/user/2', headers=headers, json=data)
    assert response.status_code == 200
    response = response.json()
    assert response['alcohol_id'] == 2
    assert response['name'] == 'Soplica Szlachetna Wódka'
    assert response['year'] == 25
    assert response['foods'] == [
        {
            'id': 1,
            'name': 'białe mięso'
        },
        {
            'id': 2,
            'name': 'przekąski'
        }
    ]
    assert response['ingredients'] == [{
        'id': 1,
        'name': 'mieszanka zbóż'
    }]
