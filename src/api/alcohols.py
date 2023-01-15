from bson import ObjectId
from pymongo.database import Database
from fastapi import APIRouter, status, Depends, Query

from src.domain.common import PageInfo
from src.domain.alcohol_filter import AlcoholFilters
from src.domain.alcohol_filter import AlcoholFiltersMetadata
from src.infrastructure.database.database_config import get_db
from src.domain.alcohol_category import PaginatedAlcoholCategories
from src.infrastructure.common.validate_object_id import validate_object_id
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.domain.alcohol import Alcohol, PaginatedAlcohol, AlcoholRecommendation
from src.infrastructure.alcohol.alcohol_mappers import map_alcohols, map_alcohol
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholNotFoundException
from src.infrastructure.database.models.alcohol_filter import AlcoholFilterDatabaseHandler
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler
from src.infrastructure.database.models.alcohol_category.mappers import map_to_alcohol_category
from src.infrastructure.recommender.recommender_client import RecommenderClient, recommender_client

router = APIRouter(prefix='/alcohols', tags=['alcohol'])

translate = {
    'color': 'kolor',
    'kind': 'kategoria',
    'country': 'kraj',
    'type': 'typ',
    'food': 'jedzenie',
    'aroma': 'aromat',
    'taste': 'smak',
    'finish': 'finisz'
}


@router.post(
    path='',
    response_model=PaginatedAlcohol,
    status_code=status.HTTP_200_OK,
    summary='Search for alcohols by phrase',
    response_model_by_alias=False,
)
async def search_alcohols(
        limit: int = 10,
        offset: int = 0,
        filters: AlcoholFilters | None = None,
        phrase: str | None = Query(default=None, min_length=3),
        db: Database = Depends(get_db)
):
    """
    Search for alcohols with pagination. Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **phrase**: str - default None, if given then phrase needs to have min 3 characters
    """
    alcohols, total = await AlcoholDatabaseHandler.search_alcohols(db.alcohols, limit, offset, phrase, filters)
    alcohols = map_alcohols(alcohols, db.alcohol_categories)
    return PaginatedAlcohol(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/filters',
    response_model=AlcoholFiltersMetadata,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol filters'
)
async def get_alcohol_filters(db: Database = Depends(get_db)):
    db_filters = await AlcoholFilterDatabaseHandler.get_all_filters(db.alcohol_filters)
    filters = []
    categories = await AlcoholCategoryDatabaseHandler.get_categories(db.alcohol_categories, 0, 0)
    for db_filter in db_filters:
        filter_dict = {
            'name': 'kind',
            'display_name': translate['kind'],
            'value': db_filter.pop('_id'),
            'filters': []
        }
        for key, values in db_filter.items():
            filter_dict['filters'].append({
                'name': key,
                'display_name': translate[key],
                'values': [value for value in values if value != '']
            })
        for category in categories:
            if category['title'] == filter_dict['value']:
                properties = category['properties']
                for kind_property in properties:
                    if kind_property != 'kind' and \
                            any(x in properties[kind_property]['bsonType'] for x in ['array', 'string']):
                        if kind_property != "temperature":
                            filter_dict['filters'].append({
                                'name': kind_property,
                                'display_name': properties[kind_property]['title'],
                                'values': await AlcoholDatabaseHandler.search_values(
                                    kind_property, db.alcohols, 0, 0, ""
                                )
                            })
        filters.append(filter_dict)
    return AlcoholFiltersMetadata(
        filters=filters
    )


@router.get(
    path='/{barcode}',
    response_model=Alcohol,
    response_model_by_alias=False,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol information by barcode'
)
async def get_alcohol_by_barcode(barcode: str, db: Database = Depends(get_db)):
    """
    Read alcohol by barcode
    """
    db_alcohol = await AlcoholDatabaseHandler.get_alcohol_by_barcode(db.alcohols, [barcode])
    if not db_alcohol:
        raise AlcoholNotFoundException()
    return map_alcohol(db_alcohol, db.alcohol_categories)


@router.get(
    path='/metadata/categories',
    response_model=PaginatedAlcoholCategories,
    status_code=status.HTTP_200_OK,
    summary='Read alcohol categories schema',
    response_model_by_alias=False
)
async def get_schemas(
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
):
    alcohol_categories = [
        map_to_alcohol_category(db_alcohol_category) for db_alcohol_category in
        await AlcoholCategoryDatabaseHandler.get_categories(db.alcohol_categories, limit, offset)
    ]
    total = await AlcoholCategoryDatabaseHandler.count_categories(db.alcohol_categories)
    return PaginatedAlcoholCategories(
        categories=alcohol_categories,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.get(
    path='/{alcohol_id}/similar',
    response_model=AlcoholRecommendation,
    status_code=status.HTTP_200_OK,
    summary='Get similar alcohols',
    response_model_by_alias=False,
)
async def get_similar(
        alcohol_id: str,
        client: RecommenderClient = Depends(recommender_client),
        db: Database = Depends(get_db)
):
    alcohol_id = str(validate_object_id(alcohol_id))
    similar = [
        ObjectId(alcohol_id) for alcohol_id in
        client.fetch_similar_alcohols(alcohol_id)['similar']
    ]
    similar = await AlcoholDatabaseHandler.get_alcohols_by_ids(db.alcohols, similar)
    return AlcoholRecommendation(
        alcohols=similar
    )


@router.post(
    path='/search_values',
    status_code=status.HTTP_200_OK,
    summary='Search for values by phrase',
)
async def search_values(
        field_name: str,
        phrase: str | None = Query(default=None),
        limit: int = 10,
        offset: int = 0,
        db: Database = Depends(get_db)
) -> list[str]:
    """
    Search for values Query params:
    - **limit**: int - default 10
    - **offset**: int - default 0
    - **phrase**: str - default None return all values
    """
    return await AlcoholDatabaseHandler.search_values(field_name, db.alcohols, limit, offset, phrase)
