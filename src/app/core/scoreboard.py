from sqlalchemy import func
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

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
from app.logger import global_logger
from app.utils.get_id_by_code import _get_id_by_code


SHEET_NAMES = ['LAM_NONG', 'VUOT_DEO', 'BUT_PHA', 'NUOC_RUT']
MEDIA_TYPE = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'



async def get_cumulative_timeline_scoreboard_export_to_excel_file_from_db(match_code: str, session: AsyncSession) -> StreamingResponse:
    """
    Export cumulative D score per question for each player in a given match to Excel,
    grouped by inferred round (from question_code prefix), sorted by created_at (actual play order).
    """
    global_logger.info(f"Exporting cumulative score timeline by actual order for match={match_code}.")
    try:
        buffer = io.BytesIO()
        response_name = f'OGD3_{match_code}_score_timeline_by_round.xlsx'

        # 1️⃣ Query records, ordered by actual play time
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
            .order_by(Record.created_at.asc())  # sort by actual order of play
        )
        execution = await session.execute(records_query)
        records = execution.all()

        if not records:
            raise HTTPException(status_code=404, detail=f"No records found for match_code={match_code}")

        # 2️⃣ Infer round name from question_code prefix
        def infer_round_name(code: str) -> str:
            prefix = code[:2].upper()
            mapping = {
                "LN": "LAM_NONG",
                "LD": "LEO_DOC",
                "BP": "BUT_PHA",
                "NR": "NUOC_RUT",
            }
            return mapping.get(prefix, "KHAC")

        from collections import defaultdict
        rounds = defaultdict(list)
        for rec in records:
            round_name = infer_round_name(rec.question_code)
            rounds[round_name].append(rec)

        # 3️⃣ Write each round into its own Excel sheet
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            for round_name in SHEET_NAMES:
                if round_name not in rounds:
                    continue

                recs = rounds[round_name]
                cumulative = {}
                last_score = {}
                timeline_data = []

                for r in recs:
                    player_code = r.player_code
                    player_name = r.player_name
                    delta = int(r.d_score_earned or 0)

                    # Update cumulative per player
                    cumulative[player_code] = cumulative.get(player_code, 0) + delta

                    prev_total = last_score.get(player_code, 0)
                    diff_from_prev = cumulative[player_code] - prev_total
                    last_score[player_code] = cumulative[player_code]

                    timeline_data.append({
                        "Mã câu hỏi": r.question_code,
                        "Mã thí sinh": player_code,
                        "Tên thí sinh": player_name,
                        "Chênh lệch so với câu hỏi trước": f"{diff_from_prev:+d}",
                        "Điểm cộng dồn": cumulative[player_code]
                    })

                df = pd.DataFrame(timeline_data)
                sheet_name = str(round_name)
                df.to_excel(writer, index=False, sheet_name=sheet_name)

        buffer.seek(0)
        global_logger.info(f"✅ Exported cumulative score timeline (ordered by created_at) for match={match_code}")

        return StreamingResponse(
            content=buffer,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": f'attachment; filename="{response_name}"'}
        )

    except HTTPException:
        raise
    except Exception as e:
        global_logger.exception(f"Error exporting cumulative score timeline for match={match_code}: {e}")
        raise HTTPException(status_code=500, detail="Failed to export cumulative score timeline.")