import datetime as dt

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from app.api.request_models.user_requests import LoginRequest
from app.api.response_models.user_response import UserLoginResponse
from app.core import exceptions
from app.core.db.models import User
from app.core.db.repository.user_repository import UserRepository
from app.core.settings import settings

PASSWORD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="user/login", scheme_name="JWT")

ALGORITHM = "HS256"


class AuthenticationService:
    """User authorisation service class."""

    def __init__(self, user_repository: UserRepository = Depends()):
        self.__user_repository = user_repository

    @staticmethod
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
