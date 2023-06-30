from uuid import UUID

from fastapi import Depends

from app.api.request_models.user_requests import UserCreateRequest, UserUpdateRequest
from app.api.response_models.user_response import UserResponse
from app.core.db.models import User
from app.core.db.repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    async def register_new_user(self, user_schema: UserCreateRequest) -> UserResponse:
        """Регистрация пользователя."""
        user = User(**user_schema.dict())
        user.role = User.Role.USER
        user = await self.__user_repository.create(user)
        return user

    async def get_user_by_id(self, id: UUID) -> UserResponse:
        """Получить пользователя."""
        return await self.__user_repository.get(id)

    async def update_user(self, user_id: UUID, user_schema: UserUpdateRequest) -> UserResponse:
        """Отредактировать пользователя."""
        user = User(**user_schema.dict())

        return await self.__user_repository.update(user_id, user)
