from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response, FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.region import Region, AllRegions, RegionCreate
from src.database.models.region import RegionDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/region', tags=['region'])


@router.get(
    path='/{region}',
    response_model=AllRegions,
    status_code=status.HTTP_200_OK,
    summary='Read all region',
    dependencies=[Depends(is_admin)]
)
async def get_region(
        db: AsyncSession = Depends(get_db)
) -> AllRegions:

    region = await DatabaseHandler.get_all_regions(db)

    return AllRegions(
        region=region,
    )

@router.post(
    path='',
    summary='Create region',
    response_model=Region,
    status_code=status.HTTP_201_CREATED
)
async def post_region(region_create_payload: RegionCreate, db: AsyncSession = Depends(get_db)) -> Region:
    """
    Create region with request body:
    - **region_name**: required
    """
    await DatabaseHandler.check_if_region_exists(
        db,
        region_create_payload.region_name
    )
    return await DatabaseHandler.create_region(db, region_create_payload)
