from typing import Generic, TypeVar, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session
        
    async def get_by_id(self, obj_id: int) -> ModelType | None:
        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
    
    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
    
    async def delete(self, obj_id: int) -> bool:
        obj = await self.get_by_id(obj_id=obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True