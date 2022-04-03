import uvicorn
from fastapi import FastAPI

app = FastAPI(title="FastAPI")


@app.get("/")
def read_root():
    return {"123": "ol"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
