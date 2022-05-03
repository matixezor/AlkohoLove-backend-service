from os.path import exists

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, status, HTTPException, Response, FastAPI, File, UploadFile, Form, Query
from fastapi.responses import FileResponse
from PIL import Image
from os import remove
import PIL
import glob

from src.utils.auth_utils import is_admin
from src.domain.page_info import PageInfo
from src.database.database_config import get_db
from src.domain.alcohol import PaginatedAlcoholInfo, Alcohol, AlcoholCreate
from src.database.models.alcohol import AlcoholDatabaseHandler as DatabaseHandler

IMAGEDIR = "../alcohol-images/"

router = APIRouter(prefix='/alcohol', tags=['alcohol'])


@router.get(
    path='',
    response_model=PaginatedAlcoholInfo,
    status_code=status.HTTP_200_OK,
    summary='[For admin] Read full alcohol information',
    dependencies=[Depends(is_admin)]
)
async def get_alcohols(
        limit: int = 10,
        offset: int = 0,
        db: AsyncSession = Depends(get_db)
) -> PaginatedAlcoholInfo:
    """
    Read alcohols with pagination
    """
    alcohols = await DatabaseHandler.get_alcohols(db, limit, offset)
    total = await DatabaseHandler.count_alcohols(db)
    return PaginatedAlcoholInfo(
        alcohols=alcohols,
        page_info=PageInfo(
            limit=limit,
            offset=offset,
            total=total
        )
    )


@router.delete(
    path='/{alcohol_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='Delete alcohol'
)
async def delete_self(
        alcohol_id: int,
        db: AsyncSession = Depends(get_db)
) -> None:
    """
    Delete alcohol by alcohol_id
    """

    await DatabaseHandler.delete_alcohol(db, alcohol_id)


@router.get(
    path='/{barcode}',
    response_model=Alcohol,
    status_code=status.HTTP_200_OK,
    summary='Read full alcohol information'
)
async def get_alcohol(
        barcode: str,
        db: AsyncSession = Depends(get_db)
) -> PaginatedAlcoholInfo:
    """
    Read alcohol by barcode
    """
    alcohol = await DatabaseHandler.get_alcohol(db, barcode)
    if not alcohol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Alcohol not found'
        )
    return alcohol


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_admin)],
    summary='Create alcohol'
)
async def create_alcohol(
        alcohol_create_payload: AlcoholCreate,
        db: AsyncSession = Depends(get_db),
) -> None:
    try:
        await DatabaseHandler.create_alcohol(db, alcohol_create_payload)
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')


@router.post(
    '/uploadimage',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_admin)],
    summary='upload alcohol image'
)
async def upload_image(image_name: str = Form(...), file: UploadFile = File(...)):
    # contents = await file.read()
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=406, detail="Only .jpeg or .png  files allowed")

    image_sm = Image.open(file.file).convert('RGB')
    image_md = Image.open(file.file).convert('RGB')
    image_sm.thumbnail(size=(400, 400))
    image_sm.save(f"{IMAGEDIR}{image_name}_sm.jpg")

    image_md.thumbnail(size=(1000, 1000))
    image_md.save(f"{IMAGEDIR}{image_name}_md.jpg")


@router.get(
    '/getimage/{image_name}',
    status_code=status.HTTP_200_OK,
    # dependencies=[Depends(is_admin)],
    summary='get alcohol image'
)
async def get_image(image_name: str):
    if exists(f"{IMAGEDIR}{image_name}.jpg"):
        return FileResponse(f"{IMAGEDIR}{image_name}.jpg")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')


# @router.get(
#     path='/getimage',
#     status_code=status.HTTP_200_OK,
#     summary='get random image'
# )
# async def read_random_file():
#     # get a random file from the image directory
#
#     random_index = randint(0, len(files) - 1)
#
#     path = f"{IMAGEDIR}{files[random_index]}"
#
#     # notice you can use FileResponse now because it expects a path
#     return FileResponse(path)

# @router.post(
#     '',
#     response_class=Response,
#     status_code=status.HTTP_201_CREATED,
#     dependencies=[Depends(is_admin)],
#     summary='Create alcohol'
# )
# async def create_alcohol(
#         alcohol_create_payload: AlcoholCreate = Depends(),
#         db: AsyncSession = Depends(get_db),
#         file: UploadFile = File(...)
# ) -> None:
#     alcohol_create_payload = alcohol_create_payload.dict()
#     try:
#         await DatabaseHandler.create_alcohol(db, alcohol_create_payload)
#     except IntegrityError:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid payload')
#
#     contents = await file.read()
#     save_file('test', contents)
