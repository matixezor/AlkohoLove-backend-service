from pytest import mark
from httpx import AsyncClient


TEST_PASSWORD_FIXTURE = 'TestTest1234'
TEST_INVALID_PASSWORD_FIXTURE = 'Test'
TEST_USERNAME_FIXTURE = 'admin'
TEST_EMAIL_FIXTURE = 'user@user.com'


@mark.asyncio
async def test_login_with_valid_credentials(async_client: AsyncClient):
    data = {
        'username': TEST_USERNAME_FIXTURE,
        'password': 'JanJan123'
    }
    response = await async_client.post('/auth/token', data=data)
    assert response.status_code == 200


@mark.asyncio
async def test_logout(async_client: AsyncClient):
    # login
    data = {
        'username': TEST_USERNAME_FIXTURE,
        'password': 'JanJan123'
    }
    response = await async_client.post('/auth/token', data=data)
    assert response.status_code == 200
    response = response.json()

    # logout
    access_token = response['access_token']
    refresh_token = response['refresh_token']
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Authorization-refresh': refresh_token
    }
    response = await async_client.post('/auth/logout', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_login_with_invalid_credentials(async_client: AsyncClient):
    data = {
        'username': TEST_USERNAME_FIXTURE,
        'password': 'Jan1233'
    }
    response = await async_client.post('/auth/token', data=data)
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Invalid username or password'
    }


@mark.asyncio
async def test_refresh_without_token(async_client: AsyncClient):
    response = await async_client.post('/auth/refresh')
    assert response.status_code == 401
    assert response.json() == {
        'detail': 'Missing Authorization Header'
    }


@mark.asyncio
@mark.parametrize(
    'username,email,password',
    [
        (None, TEST_EMAIL_FIXTURE, TEST_PASSWORD_FIXTURE),
        (TEST_USERNAME_FIXTURE, None, TEST_PASSWORD_FIXTURE),
        (TEST_USERNAME_FIXTURE, TEST_EMAIL_FIXTURE, None),
        (TEST_USERNAME_FIXTURE, TEST_EMAIL_FIXTURE, TEST_INVALID_PASSWORD_FIXTURE)
    ]
)
async def test_register_with_invalid_request_body(
        async_client: AsyncClient,
        username: str | None,
        email: str | None,
        password: str | None
):
    data = {
        'username': username,
        'email': email,
        'password': password
    }
    response = await async_client.post('/auth/register', json=data)
    assert response.status_code == 422


@mark.asyncio
@mark.parametrize(
    'username,email',
    [
        (TEST_USERNAME_FIXTURE, 'user@user.com'),
        ('test', 'admin@gmail.com')
    ]
)
async def test_register_with_existing_user(
        async_client: AsyncClient,
        username: str,
        email: str
):
    data = {
        'username': username,
        'email': email,
        'password': 'TestTest1234'
    }
    response = await async_client.post('/auth/register', json=data)
    assert response.status_code == 400
    assert response.json() == {
        'detail': f'User already exists'
    }


@mark.asyncio
async def test_register(async_client: AsyncClient):
    data = {
        'username': 'test',
        'email': 'test@gmail.com',
        'password': TEST_PASSWORD_FIXTURE
    }
    response = await async_client.post('/auth/register', json=data)
    assert response.status_code == 201
