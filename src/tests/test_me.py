from pytest import mark
from httpx import AsyncClient


@mark.asyncio
@mark.parametrize(
    'method',
    ['get', 'put', 'delete']
)
async def test_endpoints_without_token(
        method: str,
        async_client: AsyncClient
):
    response = await getattr(async_client, method)('/me')
    assert response.status_code == 401


@mark.asyncio
async def test_update_self_with_taken_email(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        'email': 'admin@gmail.com'
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me', headers=headers, json=data)
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Account with given email already exists'
    }


@mark.asyncio
async def test_update_self_with_invalid_new_password(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        'password': 'Test',
        'new_password': 'Test'
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me', headers=headers, json=data)
    assert response.status_code == 422
    response = response.json()
    assert response['detail'][0]['msg'] == 'New password does not comply with rules'


@mark.asyncio
@mark.parametrize(
    'password,new_password',
    [
        ('Test1234', None),
        (None, 'Testtest1234')
    ]
)
async def test_update_self_with_only_one_password(
        password: str | None,
        new_password: str | None,
        async_client: AsyncClient,
        user_token: str
):
    data = {
        'password': password,
        'new_password': new_password
    }
    # omit None
    data = {key: value for key, value in data.items() if value}
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Both password must be provided'


@mark.asyncio
async def test_get_self(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get('/me', headers={'Authorization': f'Bearer {user_token}'})
    assert response.status_code == 200
    response = response.json()
    assert response['username'] == 'Adam_Skorupa'
    assert response['email'] == 'adam.skorupa@gmail.com'


@mark.asyncio
@mark.parametrize(
    'data',
    [
        {
            'password': 'JanJan123',
            'new_password': 'JanJan123'
        },
        {
            'email': 'adam.skorupa@gmail.com'
        }
    ]
)
async def test_update_self(
        data: dict,
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me', headers=headers, json=data)
    assert response.status_code == 200
    response = response.json()
    assert response['username'] == 'Adam_Skorupa'
    assert response['email'] == 'adam.skorupa@gmail.com'


@mark.asyncio
async def test_update_self_with_password_not_matched_in_db(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        'password': 'Jan123',
        'new_password': 'TestTest1234'
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Passwords do not match'


@mark.asyncio
async def test_delete_self(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.delete('/me', headers=headers)
    assert response.status_code == 204
