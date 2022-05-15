from pytest import mark
from httpx import AsyncClient


@mark.asyncio
async def test_get_your_wishlist(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/me/wishlist', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['alcohols'][0]['alcohol']['alcohol_id'] == 2
    assert response['alcohols'][0]['alcohol']['name'] == 'Soplica Szlachetna Wódka'
    assert response['alcohols'][0]['alcohol']['kind'] == 'wódka'
    assert response['alcohols'][0]['alcohol']['type'] == 'czysta'
    assert response['alcohols'][0]['alcohol']['alcohol_by_volume'] == 40
    assert response['alcohols'][0]['alcohol']['manufacturer'] == 'Soplica'
    assert response['alcohols'][0]['alcohol']['rating'] == 4.0
    assert response['alcohols'][0]['alcohol']['image_name'] == 'soplica_szlachetna_wodka'
    assert len(response['alcohols']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0


@mark.asyncio
async def test_get_your_favourites(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/me/favourites', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['alcohols'][0]['alcohol']['alcohol_id'] == 1
    assert response['alcohols'][0]['alcohol']['name'] == 'Żywiec białe'
    assert response['alcohols'][0]['alcohol']['kind'] == 'piwo'
    assert response['alcohols'][0]['alcohol']['type'] == 'witbier'
    assert response['alcohols'][0]['alcohol']['alcohol_by_volume'] == 4.9
    assert response['alcohols'][0]['alcohol']['manufacturer'] == 'Żywiec'
    assert response['alcohols'][0]['alcohol']['rating'] == 5.0
    assert response['alcohols'][0]['alcohol']['image_name'] == 'zywiec_biale'
    assert len(response['alcohols']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0


@mark.asyncio
async def test_get_your_search_history(
        async_client: AsyncClient,
        admin_token: str
):
    response = await async_client.get(
        '/me/search_history', headers={'Authorization': f'Bearer {admin_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['alcohols'][0]['alcohol']['alcohol_id'] == 2
    assert response['alcohols'][0]['alcohol']['name'] == 'Soplica Szlachetna Wódka'
    assert response['alcohols'][0]['alcohol']['kind'] == 'wódka'
    assert response['alcohols'][0]['alcohol']['type'] == 'czysta'
    assert response['alcohols'][0]['alcohol']['alcohol_by_volume'] == 40
    assert response['alcohols'][0]['alcohol']['manufacturer'] == 'Soplica'
    assert response['alcohols'][0]['alcohol']['rating'] == 4.0
    assert response['alcohols'][0]['alcohol']['image_name'] == 'soplica_szlachetna_wodka'
    assert response['alcohols'][1]['alcohol']['alcohol_id'] == 1
    assert response['alcohols'][1]['alcohol']['name'] == 'Żywiec białe'
    assert response['alcohols'][1]['alcohol']['kind'] == 'piwo'
    assert response['alcohols'][1]['alcohol']['type'] == 'witbier'
    assert response['alcohols'][1]['alcohol']['alcohol_by_volume'] == 4.9
    assert response['alcohols'][1]['alcohol']['manufacturer'] == 'Żywiec'
    assert response['alcohols'][1]['alcohol']['rating'] == 5.0
    assert response['alcohols'][1]['alcohol']['image_name'] == 'zywiec_biale'
    assert len(response['alcohols']) == 2
    assert response['page_info']['total'] == 2
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0


@mark.asyncio
async def test_get_wishlist_by_user_id(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/lists/1/wishlist', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['alcohols'][0]['alcohol']['alcohol_id'] == 2
    assert response['alcohols'][0]['alcohol']['name'] == 'Soplica Szlachetna Wódka'
    assert response['alcohols'][0]['alcohol']['kind'] == 'wódka'
    assert response['alcohols'][0]['alcohol']['type'] == 'czysta'
    assert response['alcohols'][0]['alcohol']['alcohol_by_volume'] == 40
    assert response['alcohols'][0]['alcohol']['manufacturer'] == 'Soplica'
    assert response['alcohols'][0]['alcohol']['rating'] == 4.0
    assert response['alcohols'][0]['alcohol']['image_name'] == 'soplica_szlachetna_wodka'
    assert len(response['alcohols']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0


@mark.asyncio
async def test_get_favourites_by_user_id(
        async_client: AsyncClient,
        user_token: str
):
    response = await async_client.get(
        '/lists/1/favourites', headers={'Authorization': f'Bearer {user_token}'}
    )
    assert response.status_code == 200
    response = response.json()
    assert response['alcohols'][0]['alcohol']['alcohol_id'] == 1
    assert response['alcohols'][0]['alcohol']['name'] == 'Żywiec białe'
    assert response['alcohols'][0]['alcohol']['kind'] == 'piwo'
    assert response['alcohols'][0]['alcohol']['type'] == 'witbier'
    assert response['alcohols'][0]['alcohol']['alcohol_by_volume'] == 4.9
    assert response['alcohols'][0]['alcohol']['manufacturer'] == 'Żywiec'
    assert response['alcohols'][0]['alcohol']['rating'] == 5.0
    assert response['alcohols'][0]['alcohol']['image_name'] == 'zywiec_biale'
    assert len(response['alcohols']) == 1
    assert response['page_info']['total'] == 1
    assert response['page_info']['limit'] == 10
    assert response['page_info']['offset'] == 0


@mark.asyncio
async def test_delete_entry_from_wishlist(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/me/wishlist/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_entry_from_favourites(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/me/favourites/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_entry_from_search_history(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/me/search_history/1', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_delete_all_entries_from_search_history(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.delete('/me/search_history', headers=headers)
    assert response.status_code == 204


@mark.asyncio
async def test_add_entry_to_wishlist(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/me/wishlist/1', headers=headers)
    assert response.status_code == 201


@mark.asyncio
async def test_add_already_existing_entry_to_wishlist(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/me/wishlist/2', headers=headers)
    assert response.status_code == 400


@mark.asyncio
async def test_add_entry_to_favourites(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/me/favourites/2', headers=headers)
    assert response.status_code == 201


@mark.asyncio
async def test_add_already_existing_entry_to_favourites(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/me/favourites/1', headers=headers)
    assert response.status_code == 400


@mark.asyncio
async def test_add_entry_to_search_history(
        async_client: AsyncClient,
        admin_token: str
):
    headers = {'Authorization': f'Bearer {admin_token}'}
    response = await async_client.post('/me/search_history/1', headers=headers)
    assert response.status_code == 201
