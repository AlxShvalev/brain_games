from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi_restful.cbv import cbv

from app.api.request_models.user_requests import (
    LoginRequest,
    UserCreateRequest,
    UserUpdateRequest,
)
from app.api.response_models.user_response import UserLoginResponse, UserResponse
from app.core.services.authentication_service import AuthenticationService
from app.core.services.user_service import UserService

router = APIRouter(prefix="/users", tags=["Пользователи"])


@cbv(router)
class UserCBV:
    """Базовый класс для отображения пользователей."""

    user_service: UserService = Depends()
    authentication_service: AuthenticationService = Depends()

    @router.post(
        "/",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.CREATED,
        summary="Регистрация нового пользователя.",
        response_description="Регистрация нового пользователя.",
    )
    async def create_user(self, schema: UserCreateRequest) -> UserResponse:
        """
        Регистрация нового пользователя.

        - **username**: юзернейм пользователя;
        - **name**: имя пользователя;
        - **surname**: фамилия пользователя _(не обязательное поле)_;
        - **email**: email пользователя;
        - **password**: пароль пользователя;
        - **date_of_birth**: дата рождения пользователя _(не обязательное поле)_.
        """
        return await self.user_service.register_new_user(schema)

    @router.get(
        "/",
        response_model=list[UserResponse],
        status_code=HTTPStatus.OK,
        summary="Список пользователей.",
        response_description="Получить список зарегистрированных пользователей.",
    )
    async def get_users(self) -> list[UserResponse]:
        """
        Получить список зарегистрированных пользователей.

        - **id**: уникальный идентификатор пользователя;
        - **username**: юзернейм пользователя;
        - **name**: имя пользователя;
        - **surname**: фамилия пользователя _(не обязательное поле)_;
        - **email**: email пользователя;
        - **last_login_at**: дата и время последнего входа в систему _(не обязательное поле)_.
        """
        return await self.user_service.get_users()

    @router.get(
        "/{user_id}",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Получить пользователя",
        response_description="Получить пользователя по его id.",
    )
    async def get_user(self, user_id: UUID) -> UserResponse:
        """
        Получить пользователя по его id.

        - **id**: уникальный идентификатор пользователя;
        - **username**: юзернейм пользователя;
        - **name**: имя пользователя;
        - **surname**: фамилия пользователя _(не обязательное поле)_;
        - **email**: email пользователя;
        - **last_login_at**: дата и время последнего входа в систему _(не обязательное поле)_.
        """
        return await self.user_service.get_user_by_id(user_id)

    @router.post("/login", response_model=UserLoginResponse, status_code=HTTPStatus.OK)
    async def login(self, auth_data: LoginRequest) -> UserLoginResponse:
        """
        Аутентификация пользователя по username и паролю.

        - **access_token**: токен доступа пользователя;
        - **refresh_token**: токен для обновления токена доступа пользовтеля.
        """
        return await self.authentication_service.login(auth_data)

    @router.patch(
        "/{user_id}",
        response_model=UserResponse,
        response_model_exclude_none=True,
        status_code=HTTPStatus.OK,
        summary="Изменить данные пользователя.",
        response_description="Изменить данные пльзователя.",
    )
    async def update_user(self, user_id: UUID, user_data: UserUpdateRequest) -> UserResponse:
        """
        Изменить данные пользователя.

        - **name**: новое значение имени _(не обязательное поле)_;
        - **surname**: новое значение фамилии _(не обязательное поле)_;
        - **date_of_birth**: новое значение даты рождения _(не обязательное поле)_.
        """
        return await self.user_service.update_user(user_id, user_data)
