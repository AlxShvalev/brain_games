from datetime import date

from pydantic import EmailStr, Field, SecretStr, StrictStr

from app.api.request_models.request_base import RequestBaseModel


class UserCreateRequest(RequestBaseModel):
    """Тело запроса для регистрации пользователя."""

    username: StrictStr = Field(min_length=3, max_length=100)
    name: StrictStr = Field(min_length=1, max_length=100)
    surname: StrictStr | None
    email: EmailStr
    password: SecretStr
    date_of_birth: date | None


class UserUpdateRequest(RequestBaseModel):
    """Тело запроса для изменения пользователя."""

    name: StrictStr | None
    surname: StrictStr | None
    date_of_birth: date | None


class LoginRequest(RequestBaseModel):
    """Тело запроса для аутентификации пользователя."""

    username: StrictStr
    password: SecretStr


class ChangePasswordRequest(RequestBaseModel):
    """Тело запроса для смены пароля."""

    current_password: SecretStr
    new_password: SecretStr
