from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import RabotyagaResponse, RabotyagaCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.services.rabotyaga import RabotyagaService

router = APIRouter(prefix="/rabotyagi")

@router.post("/", response_model=RabotyagaResponse, status_code=status.HTTP_201_CREATED)
async def create_rabotyaga(rabotyaga: RabotyagaCreate, session: AsyncSession = Depends(get_async_session)):
    rabotyaga_service = RabotyagaService(session=session)
    rabotyaga = await rabotyaga_service.create(obj_in=rabotyaga.model_dump())
    return rabotyaga


@router.get("/", response_model=list[RabotyagaResponse], status_code=status.HTTP_200_OK)
async def get_rabotyags(session: AsyncSession = Depends(get_async_session)):
    rabotyaga_service = RabotyagaService(session=session)
    return await rabotyaga_service.get_all()
