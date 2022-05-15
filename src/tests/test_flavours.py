from pytest import mark
from urllib import parse
from httpx import AsyncClient


TAKEN_FOOD_NAME_FIXTURE = parse.quote('nuty korzenne')


@mark.asyncio
async def test_get_flavours_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/flavours', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_create_flavour_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.post(
        '/flavours', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_flavour_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/flavours/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_update_flavour_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.put(
        '/flavours/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_flavour_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.delete(
        '/flavours/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_flavour(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/flavours/1', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 1
    assert response['name'] == 'kolendra'


@mark.asyncio
async def test_get_flavours(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/flavours', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['flavours']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['flavours'][0]['id'] == 1
    assert response['flavours'][0]['name'] == 'kolendra'


@mark.asyncio
async def test_get_flavours_by_name(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/flavours?name=kole', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['flavours']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['flavours'][0]['id'] == 1
    assert response['flavours'][0]['name'] == 'kolendra'


@mark.asyncio
async def test_delete_flavour(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/flavours/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_create_flavour(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post(
        '/flavours?name=test_flavour', headers=headers
    )
    assert response.status_code == 201


@mark.asyncio
async def test_create_flavour_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/flavours', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_flavour_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post(
        f'/flavours?name={TAKEN_FOOD_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Flavour with given name already exists'


@mark.asyncio
async def test_update_flavour_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put(
        f'/flavours/1?name={TAKEN_FOOD_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Flavour with given name already exists'


@mark.asyncio
async def test_update_flavour_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put('/flavours/1', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_flavour(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put(
        '/flavours/2?name=nuty korzenne', headers=headers
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 2
    assert response['name'] == 'nuty korzenne'
