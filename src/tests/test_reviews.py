from pytest import mark
from httpx import AsyncClient

ALCOHOL_REVIEWS_FIXTURE = [
    {
        'review': 'ok',
        'rating': 5,
        'id': '62964f8f12ce37ef94d3cbab',
        'username': 'Adam_Skorupa',
        'date': '2022-05-13T15:22:32+00:00',
        'alcohol_id': '6288e32dd5ab6070dde8db8b'
    },
    {
        'review': 'DO DU**Y',
        'rating': 1,
        'id': '6296768d872c15947e569b97',
        'username': 'DariuszGołąbski',
        'date': '2022-05-15T12:42:32+00:00',
        'alcohol_id': '6288e32dd5ab6070dde8db8b'
    }
]

USER_REVIEWS_FIXTURE = [
    {
        'review': 'Pyszniutkie polecam',
        'rating': 5,
        'id': '62964f8f12ce37ef94d3cbaa',
        'username': 'Adam_Skorupa',
        'date': '2022-04-14T11:11:23+00:00',
        'alcohol_id': '6288e32dd5ab6070dde8db8a',
        'alcohol_name': 'Jameson',
        'kind': 'whisky'
    },
    {
        'review': 'ok',
        'rating': 5,
        'id': '62964f8f12ce37ef94d3cbab',
        'username': 'Adam_Skorupa',
        'date': '2022-05-13T15:22:32+00:00',
        'alcohol_id': '6288e32dd5ab6070dde8db8b',
        'alcohol_name': 'Jameson Caskmates Stout Edition',
        'kind': 'whisky'
    }
]

REPORTED_REVIEWS_FIXTURE = [
    {
        "review": "DO DU**Y",
        "rating": 1,
        "id": "6296768d872c15947e569b97",
        "user_id": "6288e2fdd5ab6070dde8db8d",
        "username": "DariuszGołąbski",
        "date": "2022-05-15T12:42:32+00:00",
        "alcohol_id": "6288e32dd5ab6070dde8db8b",
        "report_count": 2,
        "reporters": [
            "6288e2fdd5ab6070dde8db8c",
            "6288e2fdd5ab6070dde8db8b"
        ]
    },
    {
        "review": "BARDZO DO DU**Y",
        "rating": 1,
        "id": "6344648faa4450e6942b2965",
        "user_id": "6288e2fdd5ab6070dde8db8b",
        "username": "admin",
        "date": "2022-05-15T12:42:32+00:00",
        "alcohol_id": "6288e32dd5ab6070dde8db8c",
        "report_count": 1,
        "reporters": [
            "6288e2fdd5ab6070dde8db8b"
        ]
    }
]

BANNED_REVIEWS_FIXTURE = [
    {
        "review": "DO DU**Y!!!",
        "rating": 1,
        "_id": "6296768d872c15947e569b96",
        "user_id": "6288e2fdd5ab6070dde8db8d",
        "username": "DariuszGołąbski",
        "date": "2022-05-15T12:43:32",
        "alcohol_id": "6288e32dd5ab6070dde8db8c",
        "report_count": 2,
        "reporters": [
            "6288e2fdd5ab6070dde8db8c",
            "6288e2fdd5ab6070dde8db8b"
        ],
        "ban_date": "2022-07-31T13:54:29.672000",
        "reason": "Wulgaryzm!"
    }
]


@mark.asyncio
async def test_get_alcohol_reviews(async_client: AsyncClient):
    response = await async_client.get(
        '/reviews/6288e32dd5ab6070dde8db8b?limit=10&offset=0'
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reviews']) == 2
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2
    assert response['reviews'] == ALCOHOL_REVIEWS_FIXTURE


@mark.asyncio
async def test_get_alcohol_reviews_without_existing_alcohol(async_client: AsyncClient):
    response = await async_client.get(
        '/reviews/6288e32dd5ab6070dde8db9b?limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Alcohol not found'


@mark.asyncio
async def test_get_user_reviews(async_client: AsyncClient):
    response = await async_client.get(
        '/reviews/user/6288e2fdd5ab6070dde8db8c?limit=10&offset=0'
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reviews']) == 2
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2
    assert response['reviews'] == USER_REVIEWS_FIXTURE


@mark.asyncio
async def test_get_user_reviews_without_existing_user(async_client: AsyncClient):
    response = await async_client.get(
        '/reviews/user/6288e2fdd5ab6070dde8db7c?limit=10&offset=0'
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User not found'


@mark.asyncio
async def test_create_review(async_client: AsyncClient, user_token_headers: dict[str, str]):
    data = {
        'review': 'test',
        'rating': 4
    }
    response = await async_client.post(
        '/me/reviews/6288e32dd5ab6070dde8db8e',
        json=data,
        headers=user_token_headers
    )
    assert response.status_code == 201


@mark.asyncio
async def test_create_review_without_required_data(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post('/me/reviews/6288e32dd5ab6070dde8db8e', headers=user_token_headers)
    assert response.status_code == 422


@mark.asyncio
async def test_create_review_with_existing_name(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        "review": "test_review",
        "rating": 3
    }
    response = await async_client.post(
        '/me/reviews/6288e32dd5ab6070dde8db8b',
        json=data,
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Review already exists'


@mark.asyncio
async def test_create_review_with_wrong_rating(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        "review": "test_review",
        "rating": 8
    }
    response = await async_client.post(
        '/me/reviews/6288e32dd5ab6070dde8db8e',
        json=data,
        headers=user_token_headers
    )
    assert response.status_code == 422
    assert response.json() == {
            "detail": [
                {
                    "loc": [
                        "body",
                        "rating"
                    ],
                    "msg": "Rating should be number from 1 to 5",
                    "type": "value_error"
                }
            ]
    }


@mark.asyncio
async def test_update_review(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        'review': 'test_review',
        'rating': 1
    }
    response = await async_client.put(
        '/me/reviews/62964f8f12ce37ef94d3cbaa/alcohol/6288e32dd5ab6070dde8db8a',
        json=data,
        headers=user_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response['review'] == 'test_review'
    assert response['rating'] == 1
    assert response['_id'] == '62964f8f12ce37ef94d3cbaa'
    assert response['username'] == 'Adam_Skorupa'
    assert response['date'] == '2022-04-14T11:11:23+00:00'


@mark.asyncio
async def test_update_review_without_existing_review(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        "review": "test_review",
        "rating": 1
    }
    response = await async_client.put(
        '/me/reviews/62964f8f12ce37ef94d3cb1a/alcohol/6288e32dd5ab6070dde8db8a',
        json=data,
        headers=user_token_headers)
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Review not found'


@mark.asyncio
async def test_update_review_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    data = {
        "review": "test_review",
        "rating": 1
    }
    response = await async_client.put(
        '/me/reviews/6296768d872c15947e569b97/alcohol/6288e32dd5ab6070dde8db8b',
        json=data,
        headers=user_token_headers)
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Review does not belong to user'


@mark.asyncio
async def test_delete_review(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/me/reviews/62964f8f12ce37ef94d3cbaa/alcohol/6288e32dd5ab6070dde8db8a',
        headers=user_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_delete_review_that_does_not_belong_to_user(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/me/reviews/6296768d872c15947e569b97/alcohol/6288e32dd5ab6070dde8db8b',
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'Review does not belong to user'


@mark.asyncio
async def test_admin_delete_review(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/admin/reviews/62964f8f12ce37ef94d3cbaa/alcohol/6288e32dd5ab6070dde8db8a',
        headers=admin_token_headers
    )
    assert response.status_code == 204


@mark.asyncio
async def test_admin_delete_review_without_permissions(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.delete(
        '/admin/reviews/62964f8f12ce37ef94d3cbab/alcohol/6288e32dd5ab6070dde8db8b',
        headers=user_token_headers
    )
    assert response.status_code == 403
    response = response.json()
    assert response['detail'] == 'Insufficient permissions'


@mark.asyncio
async def test_admin_get_reported_reviews(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/reviews?limit=10&offset=0',
        headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reviews']) == 2
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2
    assert response['reviews'] == REPORTED_REVIEWS_FIXTURE


@mark.asyncio
async def test_get_reported_reviews_by_phrase(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        'admin/reviews/search?limit=10&offset=0&phrase=admi',
        headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reviews']) == 1
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 1
    assert response['reviews'] == [REPORTED_REVIEWS_FIXTURE[1]]


@mark.asyncio
async def test_get_reported_reviews_by_empty_phrase(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        'admin/reviews/search?limit=10&offset=0',
        headers=admin_token_headers
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reviews']) == 2
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 2
    assert response['reviews'] == REPORTED_REVIEWS_FIXTURE


@mark.asyncio
async def test_report_review(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/reviews/report/62964f8f12ce37ef94d3cbab',
        headers=user_token_headers
    )
    assert response.status_code == 201


@mark.asyncio
async def test_report_already_reported_review(
        async_client: AsyncClient,
        user_token_headers: dict[str, str]
):
    response = await async_client.post(
        '/me/reviews/report/6296768d872c15947e569b97',
        headers=user_token_headers
    )
    assert response.status_code == 400
    response = response.json()
    assert response['detail'] == 'User already reported review'


@mark.asyncio
async def test_admin_ban_review(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = {
        "reason": "Wulgarne słownictwo"
    }
    response = await async_client.put(
        '/admin/reviews/6296768d872c15947e569b97',
        json=data,
        headers=admin_token_headers,
    )
    assert response.status_code == 200
    response = response.json()
    assert response['review'] == 'DO DU**Y'
    assert response['rating'] == 1
    assert response['_id'] == '6296768d872c15947e569b97'
    assert response['user_id'] == '6288e2fdd5ab6070dde8db8d'
    assert response['username'] == 'DariuszGołąbski'
    assert response['date'] == '2022-05-15T12:42:32+00:00'
    assert response['alcohol_id'] == '6288e32dd5ab6070dde8db8b'
    assert response['report_count'] == 2
    assert response['reporters'] == [
            "6288e2fdd5ab6070dde8db8c",
            "6288e2fdd5ab6070dde8db8b",
    ]
    assert response['reason'] == 'Wulgarne słownictwo'


@mark.asyncio
async def test_admin_ban_review_that_not_exists(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    data = {
        "reason": "Wulgarne słownictwo"
    }
    response = await async_client.put(
        '/admin/reviews/6296768d872c15947e569b91',
        json=data,
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'Review not found'


@mark.asyncio
async def test_admin_get_user_banned_reviews(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/reviews/ban/6288e2fdd5ab6070dde8db8d?limit=10&offset=0',
        headers=admin_token_headers,
    )
    assert response.status_code == 200
    response = response.json()
    assert len(response['reviews']) == 1
    assert response['page_info']['offset'] == 0
    assert response['page_info']['limit'] == 10
    assert response['page_info']['total'] == 1
    assert response['reviews'] == BANNED_REVIEWS_FIXTURE


@mark.asyncio
async def test_admin_get_not_existing_user_banned_reviews(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(
        '/admin/reviews/ban/6288e21dd5ab6070dde8db8d?limit=10&offset=0',
        headers=admin_token_headers,
    )
    assert response.status_code == 404
    response = response.json()
    assert response['detail'] == 'User not found'


@mark.asyncio
async def test_get_reported_review_by_id(
        async_client: AsyncClient,
        admin_token_headers: dict[str, str]
):
    response = await async_client.get(f'/admin/reviews/6296768d872c15947e569b97', headers=admin_token_headers)
    assert response.status_code == 200
    response = response.json()
    assert response == REPORTED_REVIEWS_FIXTURE[0]
