from uvicorn import run
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from src.api.auth import router as auth_router
from src.api.admin import router as admin_router
from src.api.user_list import router as list_router
from src.api.reviews import router as review_router
from src.api.alcohols import router as alcohol_router
from src.api.me import router as logged_in_user_router
from src.api.socials import router as followers_router
from src.api.reported_errors import router as reported_error_router
from src.api.alcohol_suggestion import router as suggestions_router
from src.infrastructure.config.app_config import ALLOWED_HEADERS, ALLOWED_METHODS, ALLOW_CREDENTIALS, get_settings

app = FastAPI(title='AlkohoLove-backend-service', docs_url=get_settings().DOCS_URL, redoc_url=None)

app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(alcohol_router)
app.include_router(logged_in_user_router)
app.include_router(reported_error_router)
app.include_router(review_router)
app.include_router(list_router)
app.include_router(followers_router)
app.include_router(suggestions_router)


@app.exception_handler(AuthJWTException)
def auth_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={'detail': exc.message}
    )


if __name__ == '__main__':
    run('main:app', host='127.0.0.1', port=8080, reload=True)
