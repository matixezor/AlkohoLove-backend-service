from pytest import mark
from httpx import AsyncClient


REPORTED_ERROR_ID_FIXTURE = '507f191e810c19729de860ea'
REPORTED_DESCRIPTION_FIXTURE = 'This app sucks'
USER_ID_FIXTURE = '6288e2fdd5ab6070dde8db8b'
ALCOHOL_FIXTURE = {
    'name': 'test_name',
    'kind': 'whisky',
    'type': 'test_type',
    'alcohol_by_volume': 40.0,
    'description': 'test_description',
    'color': 'test_color',
    'manufacturer': 'test_manufacturer',
    'country': 'test_country',
    'region': 'test_region',
    'food': [],
    'finish': [],
    'aroma': [],
    'taste': [],
    'keywords': [],
    'barcode': ['123456789'],
    'age': 12
}
ALCOHOL_ID_FIXTURE = '6288e32dd5ab6070dde8db8f'


@mark.asyncio
async def test_get_users(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/users?limit=1&offset=0', headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 4
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['users'][0]['id'] == USER_ID_FIXTURE
    assert response['users'][0]['username'] == 'admin'
    assert response['users'][0]['email'] == 'admin@gmail.com'
    assert response['users'][0]['is_banned'] is not True
    assert response['users'][0]['is_admin'] is True
    assert response['users'][0]['created_on'] == '2022-03-22T19:10:25+00:00'


@mark.asyncio
async def test_get_users_by_username_search(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/users?limit=1&offset=0&username=Jeleń', headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['users'][0]['id'] == '6288e2fdd5ab6070dde8db8e'
    assert response['users'][0]['username'] == 'ZbanowanyJeleń'
    assert response['users'][0]['email'] == 'jeleń@gmail.com'
    assert response['users'][0]['is_banned'] is True
    assert response['users'][0]['is_admin'] is not True
    assert response['users'][0]['created_on'] == '2022-01-08T08:16:42+00:00'
    assert response['users'][0]['last_login'] == '2022-04-21T12:32:43+00:00'


@mark.asyncio
async def test_get_user_by_id(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/users/6288e2fdd5ab6070dde8db8e', headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == '6288e2fdd5ab6070dde8db8e'
    assert response['username'] == 'ZbanowanyJeleń'
    assert response['email'] == 'jeleń@gmail.com'
    assert response['is_banned'] is True
    assert response['is_admin'] is not True
    assert response['created_on'] == '2022-01-08T08:16:42+00:00'
    assert response['last_login'] == '2022-04-21T12:32:43+00:00'


@mark.asyncio
@mark.parametrize(
    'to_ban',
    [True, False]
)
async def test_ban_user(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str],
        to_ban: bool
):
    response = await async_client.put(
        f'/admin/users/{USER_ID_FIXTURE}?to_ban={to_ban}', headers=admin_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_get_reported_error(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/errors/{REPORTED_ERROR_ID_FIXTURE}', headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == REPORTED_ERROR_ID_FIXTURE
    assert response['description'] == REPORTED_DESCRIPTION_FIXTURE
    assert response['user_id'] == USER_ID_FIXTURE


@mark.asyncio
async def test_get_reported_error_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/errors/{REPORTED_ERROR_ID_FIXTURE}', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_reported_errors(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/errors?limit=1&offset=0', headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reported_errors']) == 1
    assert response['page_info']['total'] == 3
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['reported_errors'][0]['id'] == REPORTED_ERROR_ID_FIXTURE
    assert response['reported_errors'][0]['description'] == REPORTED_DESCRIPTION_FIXTURE
    assert response['reported_errors'][0]['user_id'] == USER_ID_FIXTURE


@mark.asyncio
async def test_get_reported_errors_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/errors/user?limit=1&offset=0', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_reported_error(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.delete(
        f'/admin/errors/{REPORTED_ERROR_ID_FIXTURE}', headers=admin_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_delete_reported_error_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        f'/admin/errors/{REPORTED_ERROR_ID_FIXTURE}', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_alcohol(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.delete('/admin/alcohols/6288e32dd5ab6070dde8db8f', headers=admin_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_create_alcohol(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.post('/admin/alcohols', headers=admin_token_headers, json=ALCOHOL_FIXTURE)
    assert response.status_code == 201


@mark.asyncio
async def test_create_alcohol_without_data(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.post('/admin/alcohols', headers=admin_token_headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_alcohol_without_barcode(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = ALCOHOL_FIXTURE
    data['barcode'] = []
    response = await async_client.post('/admin/alcohols', headers=admin_token_headers, json=data)
    assert response.status_code == 422


@mark.asyncio
async def test_create_alcohol_with_existing_name(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = ALCOHOL_FIXTURE
    data['name'] = 'Jameson'
    response = await async_client.post('/admin/alcohols', headers=admin_token_headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol exists'


@mark.asyncio
async def test_update_alcohol_with_existing_name(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = ALCOHOL_FIXTURE
    data['name'] = 'Jameson'
    response = await async_client.put(f'/admin/alcohols/{ALCOHOL_ID_FIXTURE}', headers=admin_token_headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol exists'


@mark.asyncio
async def test_update_alcohol_with_existing_barcode(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = ALCOHOL_FIXTURE
    data['barcode'] = ['5011007003234']
    response = await async_client.put(f'/admin/alcohols/{ALCOHOL_ID_FIXTURE}', headers=admin_token_headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol exists'


@mark.asyncio
async def test_update_alcohol_without_required_data(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.put(f'admin/alcohols/{ALCOHOL_ID_FIXTURE}', headers=admin_token_headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_alcohol(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = {
        'age': 25,
        'food': ['test_food'],
        'color': 'czarny'
    }
    response = await async_client.put(f'admin/alcohols/{ALCOHOL_ID_FIXTURE}', headers=admin_token_headers, json=data)
    assert response.status_code == 200
    response = response.json()
    assert response['id'] == '6288e32dd5ab6070dde8db8f'
    assert response['name'] == 'Havana Cub Anejo 3 Anos Blanco'
    assert response['age'] == 25
    assert response['food'] == ['test_food']
    assert response['color'] == 'czarny'
