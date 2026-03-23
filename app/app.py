from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.db import Base, create_db_and_tables
from contextlib import asynccontextmanager
from app.exceptions import NameAlreadyTakenError, RabotyagaByIdNotFound

from app.api.rabotyaga import router as rabotyaga_router
from app.api.smena import router as smena_router
from app.api.auth import router as auth_router
import app.api.deps

@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(rabotyaga_router)
app.include_router(smena_router)
app.include_router(auth_router)

@app.exception_handler(NameAlreadyTakenError)
async def name_taken_exception_handler(request: Request, exc: NameAlreadyTakenError):
    return JSONResponse(
        status_code=400,
        content={"detail": str(exc)},
    )

@app.exception_handler(RabotyagaByIdNotFound)
async def rabotyaga_not_found_exception_handler(request: Request, exc: RabotyagaByIdNotFound):
    return JSONResponse(
        status_code=404,
        content={"detail": str(exc)},
    )

@app.get("/")
async def root():
    return {"msg": "hello"}
