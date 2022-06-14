from os import getenv
from cloudinary import config
from dotenv import find_dotenv
from functools import lru_cache
from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, BaseSettings


if getenv('ENV') == 'LOCAL':
    env_path = find_dotenv(filename='.local.env')

else:
    env_path = find_dotenv(filename='.docker.env')


class ApplicationSettings(BaseSettings):
    DATABASE_URL: str = getenv('DATABASE_URL')
    CLOUDINARY_CLOUD_NAME: str = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY: str = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET: str = getenv('CLOUDINARY_API_SECRET')
    SECRET_KEY: str = getenv('SECRET_KEY')
    ALCOHOL_IMAGES_DIR: str = getenv('ALCOHOL_IMAGES_DIR')
    ALGORITHM: str = getenv('ALGORITHM')

    class Config:
        env_file = f'{env_path}'


@lru_cache()
def get_settings():
    return ApplicationSettings()


DATABASE_URL = getenv('DATABASE_URL')
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
ALCOHOL_IMAGES_DIR = getenv('ALCOHOL_IMAGES_DIR')
ALLOWED_ORIGINS = ['*']
ALLOWED_METHODS = ['*']
ALLOWED_HEADERS = ['*']
ALLOW_CREDENTIALS = False

config(
    cloud_name=get_settings().CLOUDINARY_CLOUD_NAME,
    api_key=get_settings().CLOUDINARY_API_KEY,
    api_secret=get_settings().CLOUDINARY_API_SECRET
)


class Settings(BaseModel):
    authjwt_secret_key: str = get_settings().SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()
