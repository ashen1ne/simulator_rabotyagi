from app.services.base import BaseService
from app.models import Rabotyaga
from sqlalchemy.ext.asyncio import AsyncSession

class RabotyagaService(BaseService[Rabotyaga]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Rabotyaga, session=session)
        
    