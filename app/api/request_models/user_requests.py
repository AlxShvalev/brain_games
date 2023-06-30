from datetime import date

from pydantic import BaseModel, EmailStr, Field, SecretStr, StrictStr


class UserCreateRequest(BaseModel):
    """Модель запроса для регистрации пользователя."""

    username: StrictStr = Field(min_length=3, max_length=100)
    name: StrictStr = Field(min_length=1, max_length=100)
    email: EmailStr
    password: SecretStr


class UserUpdateRequest(BaseModel):
    """Модель запроса для изменения пользователя."""

    name: StrictStr
    surname: StrictStr | None
    date_of_birth: date | None
