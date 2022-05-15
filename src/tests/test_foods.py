from pytest import mark
from urllib import parse
from httpx import AsyncClient


TAKEN_FOOD_NAME_FIXTURE = parse.quote('przekąski')


@mark.asyncio
async def test_get_foods_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/foods', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_create_food_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.post(
        '/foods', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_food_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/foods/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_update_food_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.put(
        '/foods/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_food_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.delete(
        '/foods/1', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_food(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/foods/1', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 1
    assert response['name'] == 'białe mięso'


@mark.asyncio
async def test_get_foods(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/foods', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['foods']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['foods'][0]['id'] == 1
    assert response['foods'][0]['name'] == 'białe mięso'


@mark.asyncio
async def test_get_foods_by_name(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/foods?name=bia', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['foods']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['foods'][0]['id'] == 1
    assert response['foods'][0]['name'] == 'białe mięso'


@mark.asyncio
async def test_delete_food(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/foods/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_create_food(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/foods?name=test_food', headers=headers)
    assert response.status_code == 201


@mark.asyncio
async def test_create_food_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/foods', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_food_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post(
        f'/foods?name={TAKEN_FOOD_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Food with given name already exists'


@mark.asyncio
async def test_update_food_with_existing_name(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put(
        f'/foods/1?name={TAKEN_FOOD_NAME_FIXTURE}', headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Food with given name already exists'


@mark.asyncio
async def test_update_food_without_required_data(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put('/foods/1', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_food(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.put('/foods/2?name=przekąski', headers=headers)
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == 2
    assert response['name'] == 'przekąski'
