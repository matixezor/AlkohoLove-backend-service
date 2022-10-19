from pytest import mark
from httpx import AsyncClient

from src.tests.response_fixtures.alcohol_suggestions import SUGGESTION_ID_FIXTURE, SUGGESTIONS_RESPONSE_FIXTURE, \
    NON_EXISTING_ID_FIXTURE

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
async def test_search_users(
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
async def test_search_users_by_username(
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
async def test_get_user(
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
async def test_get_non_existing_user(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/users/629d086dcaf272ea1d806ab4', headers=admin_token_headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User not found'


@mark.asyncio
async def test_get_user_invalid_object_id(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/users/1', headers=admin_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == '1 is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string'


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
async def test_get_error(
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
async def test_get_error_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        f'/admin/errors/{REPORTED_ERROR_ID_FIXTURE}', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_get_errors(
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
async def test_get_errors_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/errors/user?limit=1&offset=0', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_error(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.delete(
        f'/admin/errors/{REPORTED_ERROR_ID_FIXTURE}', headers=admin_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_delete_error_with_insufficient_permissions(
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
    data = ALCOHOL_FIXTURE.copy()
    data['barcode'] = []
    response = await async_client.post('/admin/alcohols', headers=admin_token_headers, json=data)
    assert response.status_code == 422


@mark.asyncio
async def test_update_alcohol_without_required_data(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.put(f'admin/alcohols/{ALCOHOL_ID_FIXTURE}', headers=admin_token_headers)
    assert response.status_code == 422


# --------------------------------------------alcohol_suggestions---------------------------------------------
@mark.asyncio
async def test_get_suggestions_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/suggestions', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_suggestion_with_insufficient_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        f'/admin/suggestions/{SUGGESTION_ID_FIXTURE}', headers=user_token_headers
    )
    assert response.status_code == 403


@mark.asyncio
async def test_delete_suggestion(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.delete(f'/admin/suggestions/{SUGGESTION_ID_FIXTURE}', headers=admin_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_get_suggestions(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get('/admin/suggestions?limit=1&offset=0', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['suggestions']) == 1
    assert response['page_info']['total'] == 3
    assert response['page_info']['limit'] == 1
    assert response['page_info']['offset'] == 0
    assert response['suggestions'] == [SUGGESTIONS_RESPONSE_FIXTURE]


@mark.asyncio
async def test_get_suggestion_by_id(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(f'/admin/suggestions/{SUGGESTION_ID_FIXTURE}', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response == SUGGESTIONS_RESPONSE_FIXTURE


@mark.asyncio
async def test_get_total_suggestions_no(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get('/admin/suggestions/total', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response == 3


@mark.asyncio
async def test_get_suggestion_by_id_that_doesnt_exist(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(f'/admin/suggestions/{NON_EXISTING_ID_FIXTURE}', headers=admin_token_headers)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == "Suggestion not found"
