from uuid import UUID

from fastapi import Depends

from app.api.request_models.user_requests import (
    UserCreateRequest,
    UserUpdateRequest,
)
from app.core.db.models import User
from app.core.db.repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    async def register_new_user(self, schema: UserCreateRequest) -> User:
        """Регистрация пользователя."""
        user = User(
            username=schema.username,
            email=schema.email,
            name=schema.name,
            surname=schema.surname,
            hashed_password=self._get_hashed_password(schema.password.get_secret_value()),
            date_of_birth=schema.date_of_birth,
        )
        return await self.__user_repository.create(user)

    async def get_users(self) -> list[User]:
        """Получить список пользователей."""
        return await self.__user_repository.get_all()

    async def get_user_by_id(self, id: UUID) -> User:
        """Получить пользователя."""
        return await self.__user_repository.get(id)

    async def update_user(self, user_id: UUID, user_schema: UserUpdateRequest) -> User:
        """Отредактировать пользователя."""
        user = await self.get_user_by_id(user_id)
        user.name = user_schema.name or user.name
        user.surname = user_schema.surname or user.surname
        user.date_of_birth = user_schema.date_of_birth or user.date_of_birth

        return await self.__user_repository.update(user_id, user)
