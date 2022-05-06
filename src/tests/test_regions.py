from pytest import mark
from httpx import AsyncClient


EXISTING_REGION_PAYLOAD_FIXTURE = {
        'region_name': 'Polska',
        'country_id': 1
    }


@mark.asyncio
async def test_get_regions_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/regions', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_create_region_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.post(
        '/regions', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_region_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/regions/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_update_region_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.put(
        '/regions/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_region_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.delete(
        '/regions/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_region(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/regions/1', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 1
    assert response['name'] == 'Polska'


@mark.asyncio
async def test_get_regions(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/regions', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['regions']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['regions'][0]['id'] == 1
    assert response['regions'][0]['name'] == 'Polska'


@mark.asyncio
async def test_get_regions_by_region_name(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/regions?region_name=Po', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['regions']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['regions'][0]['id'] == 1
    assert response['regions'][0]['name'] == 'Polska'


@mark.asyncio
async def test_delete_region(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/regions/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_create_region(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    data = {
        'region_name': 'Mazowieckie',
        'country_id': 1
    }
    response = await async_client.post('/regions', headers=headers, json=data)
    assert response.status_code == 201


@mark.asyncio
async def test_create_region_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/regions', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_region_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post(
        '/regions', headers=headers, json=EXISTING_REGION_PAYLOAD_FIXTURE
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Region with given name already exists'


@mark.asyncio
async def test_update_region_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put(
        '/regions/2', headers=headers, json=EXISTING_REGION_PAYLOAD_FIXTURE
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Region with given name already exists'


@mark.asyncio
async def test_update_region_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put('/regions/1', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_region(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    # you can update an entity with same data (that's in db)
    response = await async_client.put(
        '/regions/1', headers=headers, json=EXISTING_REGION_PAYLOAD_FIXTURE
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 1
    assert response['name'] == 'Polska'
    assert response['country']['id'] == 1
    assert response['country']['name'] == 'Polska'
