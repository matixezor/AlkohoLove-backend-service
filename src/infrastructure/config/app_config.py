from os import getenv
from cloudinary import config
from dotenv import find_dotenv
from functools import lru_cache
from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseSettings, root_validator


class ApplicationSettings(BaseSettings):
    DATABASE_URL: str = getenv('DATABASE_URL')
    CLOUDINARY_CLOUD_NAME: str = getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY: str = getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET: str = getenv('CLOUDINARY_API_SECRET')
    ALCOHOL_IMAGES_DIR: str = getenv('ALCOHOL_IMAGES_DIR')
    ALCOHOL_SUGGESTION_IMAGES_DIR: str = getenv('ALCOHOL_SUGGESTION_IMAGES_DIR')
    ALGORITHM: str = getenv('ALGORITHM')
    SECRET_KEY: str = getenv('SECRET_KEY')
    authjwt_secret_key: str = ''
    HATE_SPEECH_DETECTION_SERVICE_URL: str = getenv('HATE_SPEECH_DETECTION_SERVICE_URL')

    @root_validator
    def set_authjwt_secret_key(cls, values):
        values['authjwt_secret_key'] = values['SECRET_KEY']
        return values


@lru_cache()
def get_settings():
    env = getenv('ENV')
    if env == 'LOCAL':
        return ApplicationSettings(_env_file=find_dotenv('.local.env'))
    elif env == 'DOCKER':
        return ApplicationSettings(_env_file=find_dotenv('.docker.env'))
    else:
        return ApplicationSettings()


@AuthJWT.load_config
def get_config():
    return get_settings()


ALLOWED_ORIGINS = ['*']
ALLOWED_METHODS = ['*']
ALLOWED_HEADERS = ['*']
ALLOW_CREDENTIALS = False

config(
    cloud_name=get_settings().CLOUDINARY_CLOUD_NAME,
    api_key=get_settings().CLOUDINARY_API_KEY,
    api_secret=get_settings().CLOUDINARY_API_SECRET
)
