from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.db.models import User
from app.core.db.repository.abstract_repository import AbstractRepository
from app.core.exceptions import UserNotFoundError


class UserRepository(AbstractRepository):
    """Репозиторий для работы с моделью User."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session, User)

    async def get_by_username(self, username: str) -> User:
        stmt = select(User).where(User.username == username)
        user = await self._session.execute(stmt)
        user = user.scalars().first()
        if not user:
            raise UserNotFoundError
        return user
