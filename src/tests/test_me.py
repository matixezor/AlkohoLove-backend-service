from pytest import mark
from datetime import datetime
from httpx import AsyncClient

from src.tests.response_fixtures.followers_fixtures import FOLLOWERS_FIXTURE, FOLLOWING_FIXTURE
from src.tests.response_fixtures.list_fixtures import WISHLIST_FIXTURE, FAVOURITES_FIXTURE, SEARCH_HISTORY_FIXTURE


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
        user_token_headers: dict[str, str]
):
    data = {
        'email': 'admin@gmail.com'
    }
    response = await async_client.put('/me', headers=user_token_headers, json=data)
    assert response.status_code == 400
    assert response.json() == {
        'detail': 'Taki użytkownik już istnieje.'
    }


@mark.asyncio
async def test_update_self_with_invalid_new_password(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        'password': 'Test',
        'new_password': 'Test'
    }
    response = await async_client.put('/me', headers=user_token_headers, json=data)
    assert response.status_code == 422
    response = response.json()
    assert response['detail'] == 'Hasło nie spełnia zasad.'


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
        user_token_headers: dict[str, str]
):
    data = {
        'password': password,
        'new_password': new_password
    }
    # omit None
    data = {key: value for key, value in data.items() if value}
    response = await async_client.put('/me', headers=user_token_headers, json=data)
    assert response.status_code == 422
    response = response.json()
    assert response['detail'] == 'Oba hasła muszą zostać podane.'


@mark.asyncio
async def test_get_self(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['username'] == 'Adam_Skorupa'
    assert response['id'] == '6288e2fdd5ab6070dde8db8c'
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
            'email': 'adam.skorupa2@gmail.com'
        }
    ]
)
async def test_update_self(
        data: dict,
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put('/me', headers=user_token_headers, json=data)
    assert response.status_code == 200
    response = response.json()
    assert response['username'] == 'Adam_Skorupa'
    assert response['email'] == data.get('email', 'adam.skorupa@gmail.com')


@mark.asyncio
async def test_update_self_with_password_not_matched_in_db(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        'password': 'Jan123',
        'new_password': 'TestTest1234'
    }
    response = await async_client.put('/me', headers=user_token_headers, json=data)
    assert response.status_code == 422
    response = response.json()
    assert response['detail'] == 'Stare hasło jest niepoprawne.'


@mark.asyncio
async def test_delete_self(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete('/me', headers=user_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_get_wishlist(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/wishlist', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 3
    assert response['page_info']['total'] == 3
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'] == WISHLIST_FIXTURE


@mark.asyncio
async def test_get_favourites(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/favourites', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'] == FAVOURITES_FIXTURE


@mark.asyncio
async def test_get_alcohol_lists_positive(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/list/6288e32dd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['is_in_favourites']
    assert response['is_in_wishlist']
    assert response['alcohol_tags'] == ["628f9071f32df3b39ced1a3b"]


@mark.asyncio
async def test_get_alcohol_lists_negative(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/list/6288e32dd5ab6070dde8db8f', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert not response['is_in_favourites']
    assert not response['is_in_wishlist']
    assert response['alcohol_tags'] == []


@mark.asyncio
async def test_get_search_history(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/search_history', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['alcohols'] == SEARCH_HISTORY_FIXTURE


@mark.asyncio
async def test_delete_alcohol_from_wishlist(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete('/me/wishlist/6288e32dd5ab6070dde8db8a', headers=user_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_alcohol_from_favourites(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete('/me/favourites/6288e32dd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_alcohol_from_search_history(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete('/me/search_history/6288e32dd5ab6070dde8db8a?date=2022-07-25T19:13:25Z',
                                         headers=user_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_add_alcohol_to_wishlist(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/wishlist/6288e32dd5ab6070dde8db8f', headers=user_token_headers)
    assert response.status_code == 201


@mark.asyncio
async def test_add_alcohol_to_favourites(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/favourites/6288e32dd5ab6070dde8db8f', headers=user_token_headers)
    assert response.status_code == 201


@mark.asyncio
async def test_add_alcohol_to_search_history(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/wishlist/6288e32dd5ab6070dde8db8f', headers=user_token_headers)
    assert response.status_code == 201


@mark.asyncio
async def test_alcohol_already_in_wishlist(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/wishlist/6288e32dd5ab6070dde8db8a', headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alkohol jest już w liście.'


@mark.asyncio
async def test_alcohol_already_in_favourites(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/favourites/6288e32dd5ab6070dde8db8c', headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Alkohol jest już w liście.'


# ----------------------------------------followers---------------------------------------------------------------------
@mark.asyncio
async def test_get_followers(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/followers', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == FOLLOWERS_FIXTURE


@mark.asyncio
async def test_get_following(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.get('/me/following', headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert len(response['users']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0
    assert response['users'] == FOLLOWING_FIXTURE


@mark.asyncio
async def test_add_user_to_following(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/following/6288e2fdd5ab6070dde8db8e', headers=user_token_headers)
    assert response.status_code == 201


@mark.asyncio
async def test_delete_user_from_following(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete('/me/following/6288e2fdd5ab6070dde8db8d', headers=user_token_headers)
    assert response.status_code == 204


@mark.asyncio
async def test_user_already_in_following(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/following/6288e2fdd5ab6070dde8db8b', headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Ten użytkownik jest już w obserwowanych.'


@mark.asyncio
async def test_delete_non_existing_user_from_following(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete('/me/following/6288e2fdd5ab6070dde8db8a', headers=user_token_headers)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Nie znaleziono użytkownika.'


@mark.asyncio
async def test_migrate(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        'wishlist': ['6288e32dd5ab6070dde8db8a'],
        'favourites': [],
        'search_history': [{'alcohol_id': '6288e32dd5ab6070dde8db8b', 'date': str(datetime.now())}],
        'tags': [{'tag_name': 'test_tag', 'alcohols': ['6288e32dd5ab6070dde8db8a', '6288e32dd5ab6070dde8db8b']}]
    }
    response = await async_client.post('/me/migrate', headers=user_token_headers, json=data)
    assert response.status_code == 200


@mark.asyncio
async def test_mark_review_as_helpful(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.put('/me/reviews/62964f8f12ce37ef94d3cbaa', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['review'] == 'Pyszniutkie polecam'
    assert response['helpful_count'] == 1
    assert response['helpful'] is True


@mark.asyncio
async def test_mark_review_as_unhelpful(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.put('/me/reviews/62964f8f12ce37ef94d3cbab', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['review'] == 'ok'
    assert response['helpful_count'] == 0
    assert response['helpful'] is False


@mark.asyncio
async def test_mark__own_review_as_unhelpful(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put('/me/reviews/62964f8f12ce37ef94d3cbab', headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Nie można oznaczyć swojej opinii jako pomocna.'


@mark.asyncio
async def test_mark_own_review_as_helpful(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.put('/me/reviews/62964f8f12ce37ef94d3cbaa', headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Nie można oznaczyć swojej opinii jako pomocna.'
