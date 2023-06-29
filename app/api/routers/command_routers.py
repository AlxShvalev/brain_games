from http import HTTPStatus

from fastapi import APIRouter

from app.api.request_models.command_requests import CommandCreateRequest

router = APIRouter(prefix="/commands", tags=["Команды",])


@router.post("/", response_model=CommandCreateRequest, status_code=HTTPStatus.CREATED, summary="Создать новую команду.")
async def create_command(command: CommandCreateRequest) -> CommandCreateRequest:
    """Создать команду."""
    return command


@router.get("/", status_code=HTTPStatus.OK, tags=["Get",], summary="Получить список команд.")
async def get_commands():
    """Получить список команд."""
    return [
        {
            "id": 1,
            "title": "Command 1"
        },
        {
            "id": 2,
            "title": "Command 2"}
    ]
