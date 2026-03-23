from app.api.routes import rabotyaga, auth, smena
from fastapi import APIRouter

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(rabotyaga.router)
api_router.include_router(smena.router)