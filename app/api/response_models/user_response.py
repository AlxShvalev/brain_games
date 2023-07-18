from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class UserResponse(BaseModel):
    """
    Тело ответа для модели User.

    - **id**: уникальный id пользователя в формате UUID;
    - **username**: уникальный юзернейм пользователя;
    - **name**: имя пользователя;
    - **surname**: фамилия пользователя _(необязательное поле)_;
    - **email**: email пользователя;
    - **last_login_at**: дата последнего входа в формате ISO 8601 _(необязательное поле)_.
    """

    id: UUID
    username: str
    name: str
    surname: str | None
    email: str
    last_login_at: datetime | None

    class Config:
        orm_mode = True


class UserLoginResponse(BaseModel):
    """
    Тело ответа при аутентификации.

    - **access_token**: токен доступа;
    - **refresh_token** токен для генерации нового токена доступа.
    """

    access_token: str
    refresh_token: str
