from app.services.base import BaseService
from app.models import Smena
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from app.enums import Status
from sqlalchemy import select
from app.services.rabotyaga import RabotyagaService


class SmenaService(BaseService[Smena]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Smena, session=session)
        self.rabotyaga_service = RabotyagaService(session=session)

    async def generate_2_2_schedule(self, rabotyaga_id: int, start_date: datetime, count_months: int = 2):
        await self.rabotyaga_service.get_by_id(rabotyaga_id)
        
        current_date = start_date
        end_date = start_date + timedelta(days=30 * count_months)
        
        new_shifts = []
        
        while current_date < end_date:
            for _ in range(2):
                if current_date < end_date:
                    shift = Smena(
                        rabotyaga_id=rabotyaga_id,
                        start_smena=current_date.replace(hour=8, minute=0, second=0, microsecond=0),
                        status=Status.zaplanorivona
                    )
                    new_shifts.append(shift)
                current_date += timedelta(days=1)
            
            current_date += timedelta(days=2)
        
        if new_shifts:
            self.session.add_all(new_shifts)
            await self.session.commit()
        
        return await self.get_smeny_by_rabotyaga(rabotyaga_id=rabotyaga_id)
            
    async def get_smeny_by_rabotyaga(self, rabotyaga_id: int) -> list[Smena]:
        await self.rabotyaga_service.get_by_id(rabotyaga_id)
        
        stmt = select(self.model).where(self.model.rabotyaga_id == rabotyaga_id).order_by(self.model.start_smena)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def open_smena(self, smena_id: int) -> Smena:
        smena = await self.get_by_id(obj_id=smena_id)
        if not smena or smena.actual_start:
            return smena # Либо выбросить ошибку "Смена уже открыта"
        
        smena.actual_start = datetime.now()
        smena.status = Status.active # У тебя в Enum наверняка есть такой статус
        
        await self.session.commit()
        await self.session.refresh(smena)
        return smena

    async def close_smena(self, smena_id: int) -> Smena:
        smena = await self.get_by_id(obj_id=smena_id)
        if not smena or smena.actual_end:
            return smena
        
        smena.actual_end = datetime.now()
        smena.status = Status.vipolena 
        
        smena.zarabotok = await self.calculate_earnings(smena)
        
        smena.zarabotok = await self.calculate_earnings(smena)
        await self.rabotyaga_service.add_to_balance(smena.rabotyaga_id, smena.zarabotok)
    
        await self.session.commit()
        await self.session.refresh(smena)
        return smena
    
    async def calculate_earnings(self, smena: Smena) -> float:
        rabotyaga = await self.rabotyaga_service.get_by_id(smena.rabotyaga_id)
        
        if smena.actual_start and smena.actual_end:
            delta = smena.actual_end - smena.actual_start
            hours = delta.total_seconds() / 3600
            return round(hours * rabotyaga.hourly_rate, 2)
        
        return 0.0
        
        