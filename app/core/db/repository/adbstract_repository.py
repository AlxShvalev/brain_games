import abc
from typing import Optional, TypeVar
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core import exceptions

DatabaseModel = TypeVar("DatabaseModel")


class AbstractRepository(abc.ABC):
    """Абстрактный класс. Для реализации паттерна Репозиторий."""

    def __init__(self, session: AsyncSession, model: DatabaseModel) -> None:
        self._session = session
        self._model = model

    async def get_or_none(self, instance_id: UUID) -> Optional[DatabaseModel]:
        """Получает из базы объект модели по ID. В случе отсутствия возвращает None."""
        stmt = select(self._model).where(self._model.id == instance_id)
        db_obj = await self._session.execute(stmt)
        return db_obj.scalars().first()

    async def get(self, instance_id) -> DatabaseModel:
        """Получае из базы объект модели по ID. В случае отсутствия бросает ошибку."""
        db_obj = await self.get_or_none(instance_id)
        if db_obj is None:
            raise exceptions.ObjectNotFoundError(self._model, instance_id)
        return db_obj

    async def create(self, instance: DatabaseModel) -> DatabaseModel:
        """Создает новый объект и сохраняет в базу."""
        self._session.add(instance)
        try:
            await self._session.commit()
        except IntegrityError:
            raise exceptions.ObjectAlreadyxistsError(instance)
        await self._session.refresh(instance)
        return instance

    async def update(self, instance_id: UUID, instance: DatabaseModel) -> DatabaseModel:
        """Обновляет существующий объект в базе."""
        instance.id = instance_id
        instance = await self._session.merge(instance)
        await self._session.commit()
        return instance

    async def update_all(self, instances: list[DatabaseModel]) -> list[DatabaseModel]:
        """Обновляет несколько измененных объектов модели в базе."""
        self._session.add_all(instances)
        await self._session.commit()
        return instances

    async def get_all(self) -> list[DatabaseModel]:
        """Возвращает все объекты модели из базы."""
        stmt = select(self._model)
        db_odjs = await self._session.execute(stmt)
        return db_odjs.scalars().all()
