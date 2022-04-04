import uvicorn
from fastapi import FastAPI
from src.api.users import router as users_router


app = FastAPI(title='AlkohoLove-backend-service')
app.include_router(users_router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
