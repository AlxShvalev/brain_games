from datetime import date

from pydantic import EmailStr, Field, SecretStr, StrictStr

from app.api.request_models.request_base import RequestBaseModel


class UserCreateRequest(RequestBaseModel):
    """
    Тело запроса для регистрации пользователя.

    - **username**: уникальный юзернейм пользователя;
    - **name**: имя пользователя;
    - **surname**: фамилия пользователя _(не обязательное поле)_;
    - **email**: email пользователя;
    - **password**: пароль пользователя;
    - **date_of_birth**: дата рождения в формате ISO 8601 _(не обязательное поле)_.
    """

    username: StrictStr = Field(min_length=3, max_length=100)
    name: StrictStr = Field(min_length=1, max_length=100)
    surname: StrictStr | None
    email: EmailStr
    password: SecretStr
    date_of_birth: date | None


class UserUpdateRequest(RequestBaseModel):
    """
    Тело запроса для изменения пользователя.

    Доступные для изменения поля:
    - **name**: имя пользователя _(не обязательное поле)_;
    - **surname**: фамилия пользователя _(не обязательное поле)_;
    - **date_of_birth**: дата рождения в формате ISO 8601 _(не обязательное поле)_.
    """

    name: StrictStr | None
    surname: StrictStr | None
    date_of_birth: date | None


class LoginRequest(RequestBaseModel):
    """
    Тело запроса для аутентификации пользователя.

    - **username**: юзернейм пользователя;
    - **password**: пароль пользователя.
    """

    username: StrictStr
    password: SecretStr


class ChangePasswordRequest(RequestBaseModel):
    """
    Тело запроса для смены пароля.

    - **current_password**: текущий пароль пользователя;
    - **new_password**: новый пароль пользователя.
    """

    current_password: SecretStr
    new_password: SecretStr
