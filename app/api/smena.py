from fastapi import APIRouter, Depends, status, HTTPException
from app.services.smena import SmenaService
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.schemas import SmenaResponse, ScheduleCreate
from app.models import Smena, Rabotyaga
from app.services.rabotyaga import RabotyagaService
from app.enums import Status
from app.api.deps import get_current_rabotyaga

router = APIRouter(prefix="/smeny", tags=["smeny"])

async def get_smena_by_id(
    smena_id: int, session: AsyncSession = Depends(get_async_session)
) -> Smena:
    smena_service = SmenaService(session=session)
    smena = await smena_service.get_by_id(obj_id=smena_id)
    if not smena:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Работяга по id: {smena_id} не найден",
        )

    return smena

@router.post("/generate", response_model=list[SmenaResponse], status_code=status.HTTP_201_CREATED)
async def create_grafic(
    data: ScheduleCreate,
    current_rabotyaga: Rabotyaga = Depends(get_current_rabotyaga), 
    session: AsyncSession = Depends(get_async_session)
):
    smena_service = SmenaService(session=session)
    smeny = await smena_service.generate_2_2_schedule(
        rabotyaga_id=current_rabotyaga.id, 
        start_date=data.start_date, 
        count_months=data.count_months
    )
    return smeny

@router.get("/rabotyaga", response_model=list[SmenaResponse], status_code=status.HTTP_200_OK)
async def get_smeny_by_rabotyaga(
    current_rabotyaga: Rabotyaga = Depends(get_current_rabotyaga), 
    session: AsyncSession = Depends(get_async_session)
):
    smena_service = SmenaService(session=session)
    return await smena_service.get_smeny_by_rabotyaga(rabotyaga_id=current_rabotyaga.id)

@router.get("/{smena_id}", response_model=SmenaResponse, status_code=status.HTTP_200_OK)
async def get_smena(smena: Smena = Depends(get_smena_by_id)):
    return smena

@router.patch("/{smena_id}/open", response_model=SmenaResponse)
async def open_worker_smena(
    smena_id: int, 
    current_rabotyaga: Rabotyaga = Depends(get_current_rabotyaga), 
    session: AsyncSession = Depends(get_async_session)
):
    service = SmenaService(session=session)

    smena = await service.open_smena(smena_id=smena_id, rabotyaga_id=current_rabotyaga.id)
    
    return smena


@router.patch("/{smena_id}/close", response_model=SmenaResponse)
async def close_worker_smena(
    smena_id: int, 
    current_rabotyaga: Rabotyaga = Depends(get_current_rabotyaga), 
    session: AsyncSession = Depends(get_async_session)
):
    service = SmenaService(session=session)

    smena = await service.close_smena(smena_id=smena_id, rabotyaga_id=current_rabotyaga.id)
        
    return smena


@router.get("/stats/{rabotyaga_id}")
async def get_worker_stats(
    current_rabotyaga: Rabotyaga = Depends(get_current_rabotyaga), 
    session: AsyncSession = Depends(get_async_session)
):
    smena_service = SmenaService(session=session)
    rabotyaga_service = RabotyagaService(session=session)
    
    worker = await rabotyaga_service.get_by_id(current_rabotyaga.id)
    history = await smena_service.get_smeny_by_rabotyaga(current_rabotyaga.id)
    
    if not worker:
        raise HTTPException(status_code=404, detail="Работяга не найден")

    return {
        "rabotyaga_name": worker.rabotyaga_name,
        "total_balance": worker.total_balance,
        "total_shifts_completed": len([s for s in history if s.status == Status.vipolena]),
        "history": history
    }