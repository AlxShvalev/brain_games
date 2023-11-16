from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db.db import get_async_session
from app.core.db.models import Team
from app.core.db.repository.abstract_repository import AbstractRepository


class TeamRepository(AbstractRepository):
    """Репозиторий для работы с моделью Team."""

    def __init__(self, session: AsyncSession = Depends(get_async_session)) -> None:
        super().__init__(session, Team)
