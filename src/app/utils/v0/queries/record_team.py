GET_TEAM_RECORDS_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code FROM record_team
    ),
    all_teams AS (
        SELECT DISTINCT team_id, match_code FROM record_team
    ),
    time_series AS (
        SELECT
            t.match_code,
            t.team_id,
            ts.updated_at
        FROM all_teams t
        JOIN all_timestamps ts
        ON t.match_code = ts.match_code
    ),
    score_history AS (
        SELECT
            match_code,
            team_id,
            updated_at,
            point_score,
            match_name
        FROM record_team
    ),
    merged_series AS (
        SELECT
            ts.match_code,
            ts.team_id,
            ts.updated_at,
            sh.point_score,
            sh.match_name
        FROM time_series ts
        LEFT JOIN score_history sh
        ON ts.match_code = sh.match_code
        AND ts.team_id = sh.team_id
        AND ts.updated_at = sh.updated_at
    ),
    filled_series AS (
        SELECT
            match_code,
            team_id,
            updated_at,
            COALESCE(
                MAX(point_score) FILTER (WHERE point_score IS NOT NULL) OVER (
                    PARTITION BY match_code, team_id
                    ORDER BY updated_at
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ), 0
            ) AS point_score,
            MAX(match_name) FILTER (WHERE match_name IS NOT NULL) OVER (
                PARTITION BY match_code
            ) AS match_name
        FROM merged_series
    )
    SELECT
        fs.updated_at,
        fs.match_name,
        t.team_name,
        fs.point_score
    FROM filled_series fs
    JOIN team t ON fs.team_id = t.id
    ORDER BY fs.match_code, fs.team_id, fs.updated_at;
"""


GET_TEAM_RECORDS_BY_ID_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code FROM record_team
    ),
    all_teams AS (
        SELECT DISTINCT team_id, match_code FROM record_team
    ),
    time_series AS (
        SELECT
            t.match_code,
            t.team_id,
            ts.updated_at
        FROM all_teams t
        JOIN all_timestamps ts
        ON t.match_code = ts.match_code
    ),
    score_history AS (
        SELECT
            match_code,
            team_id,
            updated_at,
            point_score,
            match_name
        FROM record_team
    ),
    merged_series AS (
        SELECT
            ts.match_code,
            ts.team_id,
            ts.updated_at,
            sh.point_score,
            sh.match_name
        FROM time_series ts
        LEFT JOIN score_history sh
        ON ts.match_code = sh.match_code
        AND ts.team_id = sh.team_id
        AND ts.updated_at = sh.updated_at
    ),
    filled_series AS (
        SELECT
            match_code,
            team_id,
            updated_at,
            COALESCE(
                MAX(point_score) FILTER (WHERE point_score IS NOT NULL) OVER (
                    PARTITION BY match_code, team_id
                    ORDER BY updated_at
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ), 0
            ) AS point_score,
            MAX(match_name) FILTER (WHERE match_name IS NOT NULL) OVER (
                PARTITION BY match_code
            ) AS match_name
        FROM merged_series
    )
    SELECT
        fs.updated_at,
        fs.match_name,
        t.team_name,
        fs.point_score
    FROM filled_series fs
    JOIN team t ON fs.team_id = t.id
    WHERE t.id = :id
    ORDER BY fs.match_code, fs.team_id, fs.updated_at;
"""


GET_TEAM_RECORDS_BY_MATCH_CODE_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code FROM record_team
    ),
    all_teams AS (
        SELECT DISTINCT team_id, match_code FROM record_team
    ),
    time_series AS (
        SELECT
            t.match_code,
            t.team_id,
            ts.updated_at
        FROM all_teams t
        JOIN all_timestamps ts
        ON t.match_code = ts.match_code
    ),
    score_history AS (
        SELECT
            match_code,
            team_id,
            updated_at,
            point_score,
            match_name
        FROM record_team
    ),
    merged_series AS (
        SELECT
            ts.match_code,
            ts.team_id,
            ts.updated_at,
            sh.point_score,
            sh.match_name
        FROM time_series ts
        LEFT JOIN score_history sh
        ON ts.match_code = sh.match_code
        AND ts.team_id = sh.team_id
        AND ts.updated_at = sh.updated_at
    ),
    filled_series AS (
        SELECT
            match_code,
            team_id,
            updated_at,
            COALESCE(
                MAX(point_score) FILTER (WHERE point_score IS NOT NULL) OVER (
                    PARTITION BY match_code, team_id
                    ORDER BY updated_at
                    ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
                ), 0
            ) AS point_score,
            MAX(match_name) FILTER (WHERE match_name IS NOT NULL) OVER (
                PARTITION BY match_code
            ) AS match_name
        FROM merged_series
    )
    SELECT
        fs.updated_at,
        fs.match_name,
        t.team_name,
        fs.point_score
    FROM filled_series fs
    JOIN team t ON fs.team_id = t.id
    WHERE fs.match_code = :match_code
    ORDER BY fs.match_code, fs.team_id, fs.updated_at;
"""