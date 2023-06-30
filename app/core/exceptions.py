from http import HTTPStatus
from uuid import UUID

from app.core.db.models import Base as DatabaseModel


class ApplicationError(Exception):
    """Исключение для внутренней бизнес-логики."""

    detail: str = "О! Какая-то неизвестная ошибка. Мы её обязательно опознаем и исправим!"


class BadRequestError(ApplicationError):
    status_code: HTTPStatus = HTTPStatus.BAD_REQUEST


class NotFoundError(ApplicationError):
    status_code: HTTPStatus = HTTPStatus.NOT_FOUND


class ObjectAlreadyxistsError(BadRequestError):
    def __init__(self, model: DatabaseModel):
        self.detail = f"Объект '{model.__repr__} уже существует."


class ObjectNotFoundError(NotFoundError):
    def __init__(self, model: DatabaseModel, object_id: UUID):
        self.detail = f"Объект '{model.__name__}' c id '{object_id}' не найден."
