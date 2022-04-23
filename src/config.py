from os import getenv
from pydantic import BaseModel
from fastapi_jwt_auth import AuthJWT


DATABASE_URL = getenv('DATABASE_URL')
SECRET_KEY = '3f23d9abf331784b834b62aa347cfaf7cd1970f0c072d9d4e8595e41f5e708c5'
ALGORITHM = 'HS256'


class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY


@AuthJWT.load_config
def get_config():
    return Settings()
