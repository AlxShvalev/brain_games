import datetime as dt
from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.api.request_models.user_requests import (
    LoginRequest,
    UserCreateRequest,
    UserUpdateRequest,
)
from app.api.response_models.user_response import UserLoginResponse
from app.core import exceptions
from app.core.db.models import User
from app.core.db.repository.user_repository import UserRepository
from app.core.settings import settings

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="user/login", scheme_name="JWT")

ALGORITHM = "HS256"


class UserService:
    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    def _get_hashed_password(self, password: str) -> str:
        """Получить хеш пароля."""
        return PASSWORD_CONTEXT.hash(password)

    def _verify_hashed_password(self, password: str, hashed_password: str) -> bool:
        return PASSWORD_CONTEXT.verify(password, hashed_password)

    async def __authenticate_user(self, auth_data: LoginRequest) -> User:
        """Аутентификация пользователя по username и паролю."""
        user = await self.__user_repository.get_by_username(auth_data.username)
        password = auth_data.password.get_secret_value()
        if not self._verify_hashed_password(password, user.hashed_password):
            raise exceptions.InvalidAuthenticationDataError
        return user

    def __create_jwt_token(self, username: str, expires_delta: int) -> str:
        """
        Создать JWT token.

        Аргументы:
            username (str) - username пользователя,
            expires_delta (int) - время жизни токена.
        """
        expire = dt.datetime.utcnow() + dt.timedelta(minutes=expires_delta)
        to_encode = {"username": username, "exp": expire}
        return jwt.encode(to_encode, settings.SECRET_KEY, ALGORITHM)

    async def login(self, auth_data: LoginRequest) -> UserLoginResponse:
        """Получить access- и refresh- токены."""
        user = await self.__authenticate_user(auth_data)
        user.last_login_at = dt.datetime.now()
        await self.__user_repository.update(user.id, user)
        return UserLoginResponse(
            access_token=self.__create_jwt_token(user.username, settings.ACCESS_TOKEN_EXPIRES_MINUTES),
            refresh_token=self.__create_jwt_token(user.username, settings.REFRESH_TOKEN_EXPIRES_MINUTES),
        )

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
