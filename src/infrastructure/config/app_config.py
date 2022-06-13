from os import getenv
from functools import lru_cache
from dotenv import load_dotenv
from async_fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel, BaseSettings

load_dotenv()

if getenv('LOCAL') == "1":
    class FastAPISettings(BaseSettings):
        DATABASE_URL: str
        CLOUDINARY_URL: str
        SECRET_KEY: str
        ALCOHOL_IMAGES_DIR: str
        ALGORITHM: str

        class Config:
            env_file = ".env"

    @lru_cache()
    def get_settings():
        return FastAPISettings()

    settings = get_settings()

    DATABASE_URL = settings.DATABASE_URL
    SECRET_KEY = settings.SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ALCOHOL_IMAGES_DIR = settings.ALCOHOL_IMAGES_DIR
    ALLOWED_ORIGINS = ['*']
    ALLOWED_METHODS = ['*']
    ALLOWED_HEADERS = ['*']
    ALLOW_CREDENTIALS = False

else:
    DATABASE_URL = getenv('DATABASE_URL')
    SECRET_KEY = getenv('SECRET_KEY')
    ALGORITHM = getenv('ALGORITHM')
    ALCOHOL_IMAGES_DIR = getenv('ALCOHOL_IMAGES_DIR')
    ALLOWED_ORIGINS = ['*']
    ALLOWED_METHODS = ['*']
    ALLOWED_HEADERS = ['*']
    ALLOW_CREDENTIALS = False


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()
