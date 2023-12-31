from http import HTTPStatus

from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi_restful.cbv import cbv

from app.api.request_models.team_requests import TeamCreateRequest
from app.api.response_models.team_response import TeamResponse
from app.core.services.authentication_service import AuthenticationService
from app.core.services.team_service import TeamService

router = APIRouter(
    prefix="/commands",
    tags=[
        "Команды",
    ],
)


@cbv(router)
class TeamCBV:
    """Класс для отображения модели Team."""

    authentication_service: AuthenticationService = Depends()
    team_service: TeamService = Depends()

    @router.post("/", response_model=TeamResponse, status_code=HTTPStatus.CREATED, summary="Создать новую команду.")
    async def create_command(
        self, team: TeamCreateRequest, token: HTTPAuthorizationCredentials = Depends(HTTPBearer())
    ) -> TeamResponse:
        """Создать команду."""
        user = await self.authentication_service.get_current_user(token.credentials)
        return await self.team_service.create_new_team(team, user)

    @router.get("/", response_model=list[TeamResponse], status_code=HTTPStatus.OK, summary="Получить список команд.")
    async def get_commands(self) -> list[TeamResponse]:
        """Получить список команд."""
        return await self.team_service.get_teams_list()
