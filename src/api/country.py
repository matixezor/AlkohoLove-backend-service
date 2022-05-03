from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response, FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.country import Country, AllCountries, CountryCreate
from src.database.models.country import CountryDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/country', tags=['country'])


@router.get(
    path='/{country}',
    response_model=AllCountries,
    status_code=status.HTTP_200_OK,
    summary='Read all countries',
    dependencies=[Depends(is_admin)]
)
async def get_country(
        db: AsyncSession = Depends(get_db)
) -> AllCountries:

    country = await DatabaseHandler.get_all_countries(db)

    return AllCountries(
        country=country,
    )

@router.post(
    path='',
    summary='Create country',
    response_model=Country,
    status_code=status.HTTP_201_CREATED
)
async def post_country(country_create_payload: CountryCreate, db: AsyncSession = Depends(get_db)) -> Country:
    """
    Create country with request body:
    - **country_name**: required
    """
    await DatabaseHandler.check_if_country_exists(
        db,
        country_create_payload.country_name
    )
    return await DatabaseHandler.create_country(db, country_create_payload)
