from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas import RabotyagaResponse, RabotyagaCreate, RabotyagaUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_async_session
from app.models import Rabotyaga
from app.services.rabotyaga import RabotyagaService

router = APIRouter(prefix="/rabotyagi")


async def get_rabotyaga_by_id(
    rabotyaga_id: int, session: AsyncSession = Depends(get_async_session)
) -> Rabotyaga:
    rabotyaga_service = RabotyagaService(session=session)
    rabotyaga = await rabotyaga_service.get_by_id(obj_id=rabotyaga_id)
    if not rabotyaga:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Работяга по id: {rabotyaga_id} не найден",
        )

    return rabotyaga


@router.post("/", response_model=RabotyagaResponse, status_code=status.HTTP_201_CREATED)
async def create_rabotyaga(
    rabotyaga: RabotyagaCreate, session: AsyncSession = Depends(get_async_session)
):
    rabotyaga_service = RabotyagaService(session=session)
    rabotyaga = await rabotyaga_service.create(obj_in=rabotyaga.model_dump())
    return rabotyaga


@router.get("/", response_model=list[RabotyagaResponse], status_code=status.HTTP_200_OK)
async def get_rabotyags(session: AsyncSession = Depends(get_async_session)):
    rabotyaga_service = RabotyagaService(session=session)
    return await rabotyaga_service.get_all()


@router.get(
    "/{rabotyaga_id}", response_model=RabotyagaResponse, status_code=status.HTTP_200_OK
)
async def get_rabotyaga(rabotyaga: Rabotyaga = Depends(get_rabotyaga_by_id)):
    return rabotyaga


@router.delete("/{rabotyaga_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rabotyaga(
    rabotyaga_id: int, session: AsyncSession = Depends(get_async_session)
):
    rabotyaga_service = RabotyagaService(session=session)
    result = await rabotyaga_service.delete(obj_id=rabotyaga_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Работяга по id: {rabotyaga_id} не найден",
        )
        
        
@router.patch("/{rabotyaga_id}", response_model=RabotyagaResponse)
async def update_rabotyaga(
    rabotyaga_id: int,
    data: RabotyagaUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    service = RabotyagaService(session)
    
    # Важно: используем exclude_unset=True
    # Это гарантирует, что в словарь попадут только те поля, 
    # которые пользователь ЯВНО передал в JSON
    update_data = data.model_dump(exclude_unset=True)
    
    updated_obj = await service.update(obj_id=rabotyaga_id, obj_in=update_data)
    
    if not updated_obj:
        raise HTTPException(status_code=404, detail="Работяга не найден")
        
    return updated_obj
