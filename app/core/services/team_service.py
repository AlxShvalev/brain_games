from fastapi import Depends

from app.api.request_models.team_requests import TeamCreateRequest
from app.core.db.models import Team, User
from app.core.db.repository.team_repository import TeamRepository


class TeamService:
    def __init__(self, team_repository: TeamRepository = Depends()) -> None:
        self.__team_repository = team_repository

    async def create_new_team(self, new_team: TeamCreateRequest, user: User) -> Team:
        team = Team(title=new_team.title, city=new_team.city, owner_id=user.id)
        return await self.__team_repository.create(team)
