from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.team import Team
from app.schema.team import *



async def get_all_teams_from_db(session: AsyncSession):
    try:
        teams_query = (
            select(Team)
            .options(joinedload(Team.players))
            .join(Team.players)
        )
        execution = await session.execute(teams_query)
        result = execution.scalars()
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
                        for p in result.players
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
            detail=f'An unexpected error occured: {e.__class__.__name__}'
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
        result = execution.scalar_one_or_none()
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
            detail=f'An unexpected error occured: {e.__class__.__name__}'
        )