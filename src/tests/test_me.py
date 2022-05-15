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
    assert response['detail'] == 'Both passwords must be provided'


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


@mark.asyncio
async def test_create_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        "tag_name": "test_tag",
        "alcohol_ids": [1]
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post('/me/user_tags', headers=headers, json=data)
    assert response.status_code == 201


@mark.asyncio
async def test_create_user_tag_with_existing_name(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        "tag_name": "Wakacje 2022",
        "alcohol_ids": [2]
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post('/me/user_tags', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag with given name already exists'


@mark.asyncio
async def test_create_user_tag_without_required_data(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post('/me/user_tags', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_get_user_tags(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.get(
        '/me/user_tags?limit=10&offset=0', headers=headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['user_tags']) == 2
    assert response['user_tags'][0]['tag_id'] == 1
    assert response['user_tags'][0]['tag_name'] == 'Wakacje 2022'
    assert response['user_tags'][1]['tag_id'] == 2
    assert response['user_tags'][1]['tag_name'] == 'Wakacje Grecja'
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2


@mark.asyncio
async def test_get_user_tag_alcohols_with_not_existing_tag_id(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.get(
        '/me/user_tags/alcohols/10?limit=10&offset=0', headers=headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'


@mark.asyncio
async def test_get_user_tag_alcohols(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.get(
        '/me/user_tags/alcohols/1?limit=10&offset=0', headers=headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 1
    assert response['alcohols'][0]['alcohol_id'] == 1
    assert response['alcohols'][0]['name'] == 'Żywiec białe'
    assert response['alcohols'][0]['kind'] == 'piwo'
    assert response['alcohols'][0]['type'] == 'witbier'
    assert response['alcohols'][0]['alcohol_by_volume'] == 4.9
    assert response['alcohols'][0]['manufacturer'] == 'Żywiec'
    assert response['alcohols'][0]['rating'] == 5
    assert response['alcohols'][0]['image_name'] == 'zywiec_biale'
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 1


@mark.asyncio
async def test_add_alcohol_to_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post(
        '/me/user_tags/alcohols/2?alcohol_id=1',
        headers=headers
    )
    assert response.status_code == 201


@mark.asyncio
async def test_add_alcohol_to_user_tag_with_existing_alcohol_in_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post(
        '/me/user_tags/alcohols/2?alcohol_id=2',
        headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alcohol already exists in given user tag'


@mark.asyncio
async def test_add_alcohol_to_user_tag_without_existing_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post(
        '/me/user_tags/alcohols/13?alcohol_id=1',
        headers=headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'


@mark.asyncio
async def test_add_alcohol_to_user_tag_without_existing_alcohol(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post(
        '/me/user_tags/alcohols/1?alcohol_id=13',
        headers=headers
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Alcohol not found'


@mark.asyncio
async def test_add_alcohol_to_user_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.post(
        '/me/user_tags/alcohols/3?alcohol_id=2',
        headers=headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag does not belong to user'


@mark.asyncio
async def test_delete_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.delete('/me/user_tags/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_user_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.delete('/me/user_tags/3', headers=headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag does not belong to user'


@mark.asyncio
async def test_delete_alcohol_from_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.delete('/me/user_tags/alcohol/2?alcohol_id=2', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_alcohol_from_user_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.delete('/me/user_tags/alcohol/3?alcohol_id=2', headers=headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag does not belong to user'


@mark.asyncio
async def test_update_user_tag(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        "tag_name": "test_name"
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me/user_tags/2', headers=headers, json=data)
    assert response.status_code == 200
    response = response.json()
    assert response['tag_id'] == 2
    assert response['tag_name'] == 'test_name'


@mark.asyncio
async def test_update_user_tag_without_existing_tag_id(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        "tag_name": "test_name2"
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me/user_tags/100', headers=headers, json=data)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User tag not found'


@mark.asyncio
async def test_update_user_tag_without_required_data(
        async_client: AsyncClient,
        user_token: str
):
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me/user_tags/2', headers=headers)
    assert response.status_code == 422


@mark.asyncio
async def test_update_user_tag_with_existing_name(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        "tag_name": "test_name",
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me/user_tags/2', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag with given name already exists'


@mark.asyncio
async def test_update_user_tag_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token: str
):
    data = {
        "tag_name": "test_name3",
    }
    headers = {'Authorization': f'Bearer {user_token}'}
    response = await async_client.put('/me/user_tags/3', headers=headers, json=data)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User tag does not belong to user'
