from app.services.base import BaseService
from app.models import Smena
from sqlalchemy.ext.asyncio import AsyncSession

class SmenaService(BaseService[Smena]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Smena, session=session)
        
    