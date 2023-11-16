from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.api.response_models.user_response import UserResponse


class TeamResponse(BaseModel):
    """
    Тело ответа для модели User.

    - **id**: уникальный id пользователя в формате UUID;
    - **title**: название команды;
    - **city**: город;
    - **email**: email пользователя;
    - **date_of_birth**: дата рождения пользователя _(необязательное поле)_;
    - **last_login_at**: дата последнего входа в формате ISO 8601 _(необязательное поле)_.
    """

    id: UUID
    title: str
    city: Optional[str]
    owner: UserResponse

    class Config:
        orm_mode = True
