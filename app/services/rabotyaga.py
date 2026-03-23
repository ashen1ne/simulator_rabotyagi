from app.services.base import BaseService
from app.models import Rabotyaga
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.exceptions import NameAlreadyTakenError, RabotyagaByIdNotFound
from app.core.security import get_password_hash


class RabotyagaService(BaseService[Rabotyaga]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Rabotyaga, session=session)

    async def find_by_name(self, name: str) -> Rabotyaga | None:
        stmt = select(self.model).where(self.model.rabotyaga_name == name)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, obj_in: dict):
        rabotyaga_exist = await self.find_by_name(obj_in["rabotyaga_name"])
        if rabotyaga_exist:
            raise NameAlreadyTakenError("Имя уже занято")

        password = obj_in.pop("password", None)
        if password:
            obj_in["hashed_password"] = get_password_hash(password=password)
        else:
            obj_in["hashed_password"] = None

        return await super().create(obj_in)

    # В классе RabotyagaService
    async def add_to_balance(self, rabotyaga_id: int, amount: float):
        rabotyaga = await self.get_by_id(rabotyaga_id)
        if rabotyaga:
            rabotyaga.total_balance += amount
            await self.session.commit()
            await self.session.refresh(rabotyaga)
