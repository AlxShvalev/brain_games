from uuid import UUID

from fastapi import Depends
from passlib.context import CryptContext

from app.api.request_models.user_requests import UserCreateRequest, UserUpdateRequest
from app.api.response_models.user_response import UserResponse
from app.core.db.models import User
from app.core.db.repository.user_repository import UserRepository

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    def _get_hashed_password(self, password: str) -> str:
        """Получить хеш пароля."""
        return PASSWORD_CONTEXT.hash(password)

    def _verify_hashed_password(self, password: str, hashed_password: str) -> bool:
        return PASSWORD_CONTEXT.verify(password, hashed_password)

    async def register_new_user(self, schema: UserCreateRequest) -> UserResponse:
        """Регистрация пользователя."""
        user = User(
            username=schema.username,
            email=schema.email,
            name=schema.name,
            surname=schema.surname,
            role=User.Role.USER,
            hashed_password=self._get_hashed_password(schema.password.get_secret_value()),
            date_of_birth=schema.date_of_birth,
        )
        return await self.__user_repository.create(user)

    async def get_user_by_id(self, id: UUID) -> UserResponse:
        """Получить пользователя."""
        return await self.__user_repository.get(id)

    async def update_user(self, user_id: UUID, user_schema: UserUpdateRequest) -> UserResponse:
        """Отредактировать пользователя."""
        user = User(**user_schema.dict())

        return await self.__user_repository.update(user_id, user)
