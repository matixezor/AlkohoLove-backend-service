from pytest import mark
from httpx import AsyncClient


TAKEN_COUNTRY_NAME_FIXTURE = 'Polska'


@mark.asyncio
async def test_get_countries_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/countries', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_create_country_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.post(
        '/countries', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_country_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/countries/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_update_country_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.put(
        '/countries/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_country_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.delete(
        '/countries/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_country(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/countries/1', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 1
    assert response['name'] == 'Polska'


@mark.asyncio
async def test_get_countries(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/countries', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['countries']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['countries'][0]['id'] == 1
    assert response['countries'][0]['name'] == 'Polska'


@mark.asyncio
async def test_get_countries_by_country_name(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/countries?country_name=Po', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['countries']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['countries'][0]['id'] == 1
    assert response['countries'][0]['name'] == 'Polska'


@mark.asyncio
async def test_delete_country(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/countries/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_create_country(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/countries?country_name=Hiszpania', headers=headers)
    assert response.status_code == 201


@mark.asyncio
async def test_create_country_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/countries', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_country_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post(
        f'/countries?country_name={TAKEN_COUNTRY_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Country with given name already exists'


@mark.asyncio
async def test_update_country_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put(
        f'/countries/2?country_name={TAKEN_COUNTRY_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Country with given name already exists'


@mark.asyncio
async def test_update_country_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put('/countries/1', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_country(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put(
        f'/countries/1?country_name={TAKEN_COUNTRY_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 1
    assert response['name'] == 'Polska'
