from PIL import Image
from os import remove
from os.path import exists
from fastapi.responses import FileResponse
from fastapi import APIRouter, Depends, status, HTTPException, Response, File, UploadFile, Form

from src.config import IMAGEDIR
from src.utils.auth_utils import is_admin


router = APIRouter(prefix='/media', tags=['media'])


@router.post(
    '',
    response_class=Response,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(is_admin)],
    summary='[For admin] Upload alcohol image'
)
async def upload_image(image_name: str = Form(...), file: UploadFile = File(...)):
    if file.content_type not in ['image/jpeg', 'image/png']:
        raise HTTPException(status_code=404, detail='Only .jpeg or .png  files allowed')

    image_sm = Image.open(file.file).convert('RGB')
    image_md = Image.open(file.file).convert('RGB')
    image_sm.thumbnail(size=(400, 400))
    image_sm.save(f'{IMAGEDIR}{image_name}_sm.jpg')

    image_md.thumbnail(size=(1000, 1000))
    image_md.save(f'{IMAGEDIR}{image_name}_md.jpg')


@router.get(
    '/{image_name}',
    status_code=status.HTTP_200_OK,
    summary='Get alcohol image'
)
async def get_image(image_name: str, size: str):
    """
    Get image by name. Specify size, either sm or md.
    """
    image_path = f'{IMAGEDIR}{image_name}_{size}.jpg'
    if exists(image_path):
        return FileResponse(image_path)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')


@router.delete(
    '/{image_name}',
    status_code=status.HTTP_204_NO_CONTENT,
    summary='[For admin] Delete alcohol image',
    dependencies=[Depends(is_admin)],
)
async def get_image(image_name: str):
    """
    Delete image by name.
    """
    image_path_md = f'{IMAGEDIR}{image_name}_md.jpg'
    image_path_sd = f'{IMAGEDIR}{image_name}_sd.jpg'
    if exists(image_path_md) and exists(image_path_sd):
        remove(image_path_md)
        remove(image_path_sd)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Image not found')
