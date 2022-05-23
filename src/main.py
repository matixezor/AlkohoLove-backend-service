from uvicorn import run
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from async_fastapi_jwt_auth.exceptions import AuthJWTException

from src.api.auth import router as auth_router
from src.api.admin import router as admin_router
from src.api.alcohols import router as alcohol_router
from src.api.me import router as logged_in_user_router
from src.api.reported_errors import router as reported_error_router
from src.infrastructure.config.app_config import \
    ALLOWED_ORIGINS, ALLOWED_HEADERS, ALLOWED_METHODS, ALLOW_CREDENTIALS, STATIC_DIR


app = FastAPI(title='AlkohoLove-backend-service')

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=ALLOW_CREDENTIALS,
    allow_methods=ALLOWED_METHODS,
    allow_headers=ALLOWED_HEADERS,
)

app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(alcohol_router)
app.include_router(logged_in_user_router)
app.include_router(reported_error_router)


@app.exception_handler(AuthJWTException)
def auth_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.message}
    )


if __name__ == '__main__':
    run('main:app', host='127.0.0.1', port=8080, reload=True)
