from fastapi import APIRouter

from app.api.request_models.user_requests import UserCreateRequest

router = APIRouter(prefix="/users", tags=["Пользователи"])


@router.post("/")
async def create_user(user_schema: UserCreateRequest) -> UserCreateRequest:
    """Создать пользователя."""
    return user_schema
