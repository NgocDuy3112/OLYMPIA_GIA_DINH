from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from valkey.asyncio import Valkey
import io
import json
import pandas as pd

from app.model.player import Player
from app.model.match import Match
from app.model.record import Record
from app.model.question import Question
from app.schema.record import *
from app.schema.scoreboard import GetScoreboardResponse
from app.logger import global_logger


MEDIA_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'



async def get_recent_cumulative_timeline_scoreboard_from_cache(match_code: str, cache: Valkey) -> GetScoreboardResponse:
    cache_key = f"scoreboard:{match_code}"
    global_logger.info(f"Attempting to retrieve scoreboard for match={match_code} from Valkey key: {cache_key}")
    try:
        scoreboard_hash = await cache.hgetall(cache_key)
        if scoreboard_hash is None:
            global_logger.info(f"Scoreboard not found in cache for match={match_code}")
            raise HTTPException(status_code=404, detail=f"Scoreboard not found in cache for match={match_code}")
        # Assuming the scoreboard is stored as a JSON string
        scoreboard_list = []
        for player_code_bytes, score_bytes in scoreboard_hash.items():
            try:
                # Decode bytes to string and convert score to integer
                player_code = player_code_bytes.decode() if isinstance(player_code_bytes, bytes) else player_code_bytes
                total_d_score = int(score_bytes.decode() if isinstance(score_bytes, bytes) else score_bytes)
                
                scoreboard_list.append({
                    "player_code": player_code,
                    "total_d_score": total_d_score,
                })
            except ValueError:
                global_logger.error(f"Invalid score value in cache for player {player_code} in match {match_code}.")
                continue
        global_logger.info(f"✅ Successfully retrieved and parsed scoreboard from cache for match={match_code}")
        return GetScoreboardResponse(
            response={
                'data': {
                    'match_code': match_code,
                    'scoreboard': scoreboard_list
                }
            }
        )
    except json.JSONDecodeError:
        global_logger.error(f"Failed to decode JSON from cache for match={match_code}. Key: {cache_key}")
        raise HTTPException(status_code=500, detail=f"Failed to decode JSON from cache for match={match_code}. Key: {cache_key}")
    except Exception as e:
        global_logger.exception(f"Error accessing Valkey for match={match_code}: {e}")
        raise HTTPException(status_code=500, detail=f"Error accessing Valkey for match={match_code}: {e}")



async def get_cumulative_timeline_scoreboard_export_to_excel_file_from_db(match_code: str, session: AsyncSession) -> StreamingResponse:
    """
    Export cumulative D score per question for each player in a given match to Excel,
    in a single sheet, sorted by created_at (actual play order).
    """
    global_logger.info(f"Exporting cumulative score timeline (single sheet) for match={match_code}.")
    try:
        buffer = io.BytesIO()
        response_name = f'OGD3_{match_code}_full_timeline_score.xlsx'

        records_query = (
            select(
                Player.player_code,
                Player.player_name,
                Question.question_code,
                Record.d_score_earned,
                Record.created_at
            )
            .join(Player, Player.id == Record.player_id)
            .join(Match, Match.id == Record.match_id)
            .join(Question, Question.id == Record.question_id)
            .where(Match.match_code == match_code)
            .order_by(Record.created_at.asc())
        )
        execution = await session.execute(records_query)
        records = execution.all()

        if not records:
            raise HTTPException(status_code=404, detail=f"No records found for match_code={match_code}")

        cumulative = {}
        timeline_data = []

        for r in records:
            player_code = r.player_code
            player_name = r.player_name
            delta = int(r.d_score_earned or 0)
            prev_total = cumulative.get(player_code, 0)
            cumulative[player_code] = prev_total + delta
            diff_from_prev = delta 
            timeline_data.append({
                "Mã câu hỏi": r.question_code,
                "Mã thí sinh": player_code,
                "Tên thí sinh": player_name,
                "Điểm thay đổi": f"{diff_from_prev:+d}",
                "Điểm cộng dồn": cumulative[player_code]
            })

        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            df = pd.DataFrame(timeline_data)
            df['Vòng thi'] = df['Mã câu hỏi'].apply(lambda x: x[:2].upper())
            df.to_excel(writer, index=False, sheet_name="SCOREBOARD")

        buffer.seek(0)
        global_logger.info(f"✅ Exported full cumulative score timeline for match={match_code}")

        return StreamingResponse(
            content=buffer,
            media_type=MEDIA_TYPE,
            headers={"Content-Disposition": f'attachment; filename="{response_name}"'}
        )

    except HTTPException:
        raise
    except Exception as e:
        global_logger.exception(f"Error exporting full cumulative score timeline for match={match_code}: {e}")
        raise HTTPException(status_code=500, detail="Failed to export full cumulative score timeline.")