from typing import Generic, TypeVar, Type, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import Base
from app.exceptions import RabotyagaByIdNotFound

ModelType = TypeVar("ModelType", bound=Base)


class BaseService(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_by_id(self, obj_id: int) -> ModelType:

        stmt = select(self.model).where(self.model.id == obj_id)
        result = await self.session.execute(stmt)
        exist = result.scalar_one_or_none()
        if not exist:
            raise RabotyagaByIdNotFound(f"Работяга по id: obj_id")
        return exist

    async def get_all(self, skip: int = 0, limit: int = 100) -> list[ModelType]:
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, obj_in: dict) -> ModelType:
        try:
            db_obj = self.model(**obj_in)
            self.session.add(db_obj)
            await self.session.commit()
            await self.session.refresh(db_obj)
            return db_obj
        except Exception as e:
            await self.session.rollback()
            raise e

    async def delete(self, obj_id: int) -> bool:
        obj = await self.get_by_id(obj_id=obj_id)
        if not obj:
            return False
        await self.session.delete(obj)
        await self.session.commit()
        return True

    async def update(self, obj_id: int, obj_in: dict) -> ModelType | None:
        db_obj = await self.get_by_id(obj_id)
        if not db_obj:
            return None

        for field, value in obj_in.items():
            if value is not None:
                setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
