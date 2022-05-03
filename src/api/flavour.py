from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response, FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.flavour import Flavour, AllFlavours, FlavourCreate
from src.database.models.flavour import FlavourDatabaseHandler as DatabaseHandler

router = APIRouter(prefix='/flavour', tags=['flavour'])


@router.get(
    path='/{flavour}',
    response_model=AllFlavours,
    status_code=status.HTTP_200_OK,
    summary='Read all flavours',
    dependencies=[Depends(is_admin)]
)
async def get_flavour(
        db: AsyncSession = Depends(get_db)
) -> AllFlavours:

    flavour = await DatabaseHandler.get_all_flavours(db)

    return AllFlavours(
        flavour=flavour,
    )

@router.post(
    path='',
    summary='Create flavour',
    response_model=Flavour,
    status_code=status.HTTP_201_CREATED
)
async def post_flavour(flavour_create_payload: FlavourCreate, db: AsyncSession = Depends(get_db)) -> Flavour:
    """
    Create flavour with request body:
    - **flavour_name**: required
    """
    await DatabaseHandler.check_if_flavour_exists(
        db,
        flavour_create_payload.flavour_name
    )
    return await DatabaseHandler.create_flavour(db, flavour_create_payload)
