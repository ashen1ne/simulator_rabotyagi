from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas import RabotyagaResponse, RabotyagaCreate
from app.services.rabotyaga import RabotyagaService
from app.security import create_access_token, verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RabotyagaResponse)
async def register(data: RabotyagaCreate, session: AsyncSession = Depends(get_async_session)):
    service = RabotyagaService(session)
    return await service.create(data.model_dump())

@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_async_session)
):
    service = RabotyagaService(session)
    worker = await service.find_by_name(form_data.username)
    
    if not worker or not worker.hashed_password:
        raise HTTPException(status_code=400, detail="Неверное имя или пароль")
    
    if not verify_password(form_data.password, worker.hashed_password):
        raise HTTPException(status_code=400, detail="Неверное имя или пароль")
    
    access_token = create_access_token(data={"sub": str(worker.id)})
    return {"access_token": access_token, "token_type": "bearer"}