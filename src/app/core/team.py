from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.team import Team
from app.schema.team import *



async def post_team_to_db(request: PostTeamRequest, session: AsyncSession) -> PostTeamResponse:
    try:
        new_team = Team(
            team_code = request.team_code,
            team_name = request.team_name
        )
        session.add(new_team)
        await session.commit()
        await session.refresh(new_team)
        return PostTeamResponse(
            response={'messsage': f'Add a team with team_code = {request.team_code} successfully!'}
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e}'
        )



async def get_all_teams_from_db(session: AsyncSession):
    try:
        teams_query = (
            select(Team)
            .options(joinedload(Team.players))
            .join(Team.players)
        )
        execution = await session.execute(teams_query)
        result = execution.unique().scalars().all()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail='No teams found!'
            )
        return GetTeamResponse(
            response={
                'data': [
                    {
                        'team_name': res.team_name,
                        'team_code': res.team_code,
                        'players': [
                            {
                                'player_name': p.player_name,
                                'player_code': p.player_code
                            }
                        for p in res.players
                        ]
                    }
                for res in result
                ]
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e}'
        )



async def get_team_from_team_code_from_db(team_code: str, session: AsyncSession):
    try:
        team_query = (
            select(Team)
            .options(joinedload(Team.players))
            .join(Team.players)
        )
        team_query = team_query.where(Team.team_code == team_code)
        execution = await session.execute(team_query)
        result = execution.unique().scalar_one_or_none()
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f'Team with team_code = {team_code} not existed.'
            )
        return GetTeamResponse(
            response={
                'data': {
                    'team_name': result.team_name,
                    'team_code': result.team_code,
                    'players': [
                        {
                            'player_name': p.player_name,
                            'player_code': p.player_code
                        }
                    for p in result.players
                    ]
                }
                
            } 
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occured: {e}'
        )