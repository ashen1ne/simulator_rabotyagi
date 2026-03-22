from fastapi import FastAPI
from app.db import Base, create_db_and_tables
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"msg": "hello"}
