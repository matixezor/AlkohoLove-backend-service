import uvicorn
from fastapi import FastAPI, status

from src.api.auth import router as auth_router
from src.api.users import router as users_router


app = FastAPI(title='AlkohoLove-backend-service')
app.include_router(auth_router)
app.include_router(users_router)


@app.get(
    path='/',
    status_code=status.HTTP_200_OK
)
def test():
    return {'hello': 'world'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
