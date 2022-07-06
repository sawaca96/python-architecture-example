from fastapi import FastAPI

from app.config import settings

app = FastAPI(root_path=settings.ROOT_PATH)


@app.get("/ping")
def ping() -> str:
    return "pong"


@app.get("/foo")
def foo() -> str:
    return "bar"
