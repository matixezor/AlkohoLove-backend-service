from os import getenv
from pydantic import BaseModel
from async_fastapi_jwt_auth import AuthJWT

DATABASE_URL = getenv('DATABASE_URL')
SECRET_KEY = getenv('SECRET_KEY')
ALGORITHM = getenv('ALGORITHM')
STATIC_DIR = getenv('STATIC_DIR', default='../static')
ALLOWED_ORIGINS = ['*']
ALLOWED_METHODS = ['*']
ALLOWED_HEADERS = ['*']
ALLOW_CREDENTIALS = False


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()
