from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.db.models import User
from app.core.db.repository.abstract_repository import AbstractRepository


class UserRepository(AbstractRepository):
    """Репозиторий для работы с моделью User."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session, User)
