from pymongo.database import Database
from fastapi import APIRouter, status, Depends, Query

from src.domain.common import PageInfo
from src.domain.alcohol_filter import AlcoholFilters
from src.domain.alcohol import Alcohol, PaginatedAlcohol
from src.domain.alcohol_filter import AlcoholFiltersMetadata
from src.infrastructure.database.database_config import get_db
from src.domain.alcohol_category import PaginatedAlcoholCategories
from src.infrastructure.database.models.alcohol import AlcoholDatabaseHandler
from src.infrastructure.alcohol.alcohol_mappers import map_alcohols, map_alcohol
from src.infrastructure.exceptions.alcohol_exceptions import AlcoholNotFoundException
from src.infrastructure.database.models.alcohol_filter import AlcoholFilterDatabaseHandler
from src.infrastructure.database.models.alcohol_category import AlcoholCategoryDatabaseHandler
from src.infrastructure.database.models.alcohol_category.mappers import map_to_alcohol_category

router = APIRouter(prefix='/alcohols', tags=['alcohol'])

translate = {
    'color': 'kolor',
    'kind': 'kategoria',
    'country': 'kraj',
    'type': 'typ',
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
