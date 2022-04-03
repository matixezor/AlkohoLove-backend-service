import uvicorn
from fastapi import FastAPI

app = FastAPI(title="FastAPI")


@app.get("/")
def read_root():
    return {"test": "test"}


if __name__ == "__main__":
    uvicorn.run("main:src", host="0.0.0.0", port=8080, reload=True)
