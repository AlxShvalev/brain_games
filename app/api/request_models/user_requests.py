from datetime import date

from pydantic import BaseModel, EmailStr, Field, SecretStr, StrictStr


class UserCreateRequest(BaseModel):
    """Модель запроса для регистрации пользователя."""

    username: StrictStr = Field(
        min_length=3, max_length=100, title="username", description="username, уникальный для каждого пользователя."
    )
    name: StrictStr = Field(min_length=1, max_length=100, title="Имя пользователя")
    surname: StrictStr | None
    email: EmailStr
    password: SecretStr
    date_of_birth: date | None


class UserUpdateRequest(BaseModel):
    """Модель запроса для изменения пользователя."""

    name: StrictStr
    surname: StrictStr | None
    date_of_birth: date | None
