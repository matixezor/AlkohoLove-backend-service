from os import getenv
from cloudinary import config
from functools import lru_cache
from pydantic import BaseSettings
from async_fastapi_jwt_auth import AuthJWT


class ApplicationSettings(BaseSettings):
    DATABASE_URL: str = getenv('DATABASE_URL')
    CLOUDINARY_CLOUD_NAME: str = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY: str = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET: str = getenv('CLOUDINARY_API_SECRET')
    ALCOHOL_IMAGES_DIR: str = getenv('ALCOHOL_IMAGES_DIR')
    ALGORITHM: str = getenv('ALGORITHM')
    authjwt_secret_key: str = getenv('SECRET_KEY')


@lru_cache()
def get_settings():
    env = getenv('ENV')
    if env == 'LOCAL':
        return ApplicationSettings(_env_file='.local.env')
    elif env == 'DOCKER':
        return ApplicationSettings(_env_file='.docker.env')
    else:
        return ApplicationSettings()


ALLOWED_ORIGINS = ['*']
ALLOWED_METHODS = ['*']
ALLOWED_HEADERS = ['*']
ALLOW_CREDENTIALS = False

config(
    cloud_name=get_settings().CLOUDINARY_CLOUD_NAME,
    api_key=get_settings().CLOUDINARY_API_KEY,
    api_secret=get_settings().CLOUDINARY_API_SECRET
)


@AuthJWT.load_config
def get_config():
    return get_settings()
