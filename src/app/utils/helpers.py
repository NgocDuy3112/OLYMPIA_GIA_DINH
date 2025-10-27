from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import NoResultFound

from uuid import UUID

from fastapi import HTTPException



async def _get_id_by_code(session: AsyncSession, model, code_field: str, code: str, entity_name: str) -> UUID:
    query = select(model.id).where(getattr(model, code_field) == code)
    try:
        execution = await session.execute(query)
        entity_id = execution.scalar_one()
        return entity_id
    except NoResultFound:
        raise HTTPException(
            status_code=404,
            detail=f'{entity_name} with {code_field}={code} not found!'
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database query failed for {entity_name} validation.")