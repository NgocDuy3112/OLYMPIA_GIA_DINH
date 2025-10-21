from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from fastapi import HTTPException

from app.model.team import Team
from app.schema.team import *
from app.logger import global_logger



async def post_team_to_db(request: PostTeamRequest, session: AsyncSession) -> PostTeamResponse:
    global_logger.info(f"POST request received to create team with code: {request.team_code}.")
    new_team = Team(
        team_code = request.team_code,
        team_name = request.team_name
    )
    session.add(new_team)
    global_logger.debug(f"Team object created and added to session. team_code={request.team_code}")
    try:
        await session.commit()
        await session.refresh(new_team)
        global_logger.info(f"Team created successfully. team_code={request.team_code}, team_id={new_team.id}")
        
        return PostTeamResponse(
            response={'message': f'Team with team_code={request.team_code} created successfully.'}
        )
    except IntegrityError:
        await session.rollback()
        global_logger.warning(f"Failed to create team due to unique constraint violation. team_code={request.team_code}. Returning 409.")
        raise HTTPException(
            status_code=409,
            detail=f'A team with team_code={request.team_code} already exists.'
        )
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during team creation/commit for team_code={request.team_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected server error occurred during team creation.'
        )



async def put_team_to_db(request: PutTeamRequest, session: AsyncSession) -> PutTeamResponse:
    global_logger.info(f"PUT request received to update team with code: {request.team_code}.")
    try:
        team_query = select(Team).where(Team.team_code == request.team_code)
        execution = await session.execute(team_query)
        team_found = execution.scalar_one_or_none()
        if team_found is None:
            raise HTTPException(status_code=404, detail="Team not found for the given team_code.")
        team_found.team_name = request.team_name
        await session.commit()
        await session.refresh(team_found)
        global_logger.info(f"Team updated successfully for team_code={request.team_code}")
        return PutTeamResponse(response={"message": "Team updated successfully!"})
    except HTTPException:
        raise
    except Exception:
        await session.rollback()
        global_logger.exception(f'Unexpected error during team update for team_code={request.team_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during team update.'
        )



async def get_all_teams_with_players_info_from_db(session: AsyncSession) -> GetTeamResponse:
    global_logger.info("GET request received for all teams with players info.")
    try:
        teams_query = (
            select(Team)
            .options(joinedload(Team.players))
        )
        execution = await session.execute(teams_query)
        result = execution.unique().scalars().all()
        
        if not result:
            global_logger.warning("No teams found in the database. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail='No teams found!'
            )
            
        global_logger.info(f"Successfully retrieved {len(result)} teams.")
        
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
    except Exception:
        global_logger.exception('Unexpected error occurred while fetching all teams.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching all teams.'
        )



async def get_team_with_players_info_from_team_code_from_db(team_code: str, session: AsyncSession) -> GetTeamResponse:
    global_logger.info(f"GET request received for team: {team_code} with players info.")
    try:
        team_query = (
            select(Team)
            .options(joinedload(Team.players))
            .where(Team.team_code == team_code)
        )
        execution = await session.execute(team_query)
        result = execution.unique().scalar_one_or_none()
        if result is None:
            global_logger.warning(f"Team not found: team_code={team_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'Team with team_code = {team_code} not found.' # Corrected detail message
            )
            
        global_logger.info(f"Successfully retrieved team: {team_code}.")
            
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
    except Exception:
        global_logger.exception(f'Unexpected error occurred while fetching team_code={team_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred while fetching team.'
        )



async def delete_team_from_team_code_from_db(team_code: str, session: AsyncSession) -> DeleteTeamResponse:
    # We don't actually delete the team, just set the is_deleted=True
    global_logger.info(f"DELETE request received for team with team_code={team_code} (soft-delete).")
    try:
        # 1. Use an efficient bulk update statement
        update_query = (
            update(Team)
            .where(Team.team_code == team_code)
            .values(is_deleted=True)
        )
        
        execution = await session.execute(update_query)
        rows_affected = execution.rowcount
        
        # 2. Commit the changes to the database
        await session.commit()
        
        # 3. Check the count of updated rows for a 404 response
        if rows_affected == 0:
            # Nothing was updated, so no need to rollback.
            global_logger.warning(f"Team not found: team_code={team_code}. Returning 404.")
            raise HTTPException(
                status_code=404,
                detail=f'No team with team_code={team_code} existed'
            )

        global_logger.info(f"Team soft-deleted successfully for team_code={team_code}")
        return DeleteTeamResponse(response={"message": "Team deleted successfully!"})

    except HTTPException:
        # Re-raise explicit HTTPExceptions (like the 404)
        raise
    except Exception:
        # Rollback on any unexpected database error
        await session.rollback()
        global_logger.exception(f'Unexpected error during team deletion for team_code={team_code}.')
        raise HTTPException(
            status_code=500,
            detail=f'An unexpected error occurred during team deletion.'
        )