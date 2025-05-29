GET_PLAYER_RECORDS_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code FROM record_player
    ),
    all_players AS (
        SELECT DISTINCT player_id, match_code FROM record_player
    ),
    time_series AS (
        SELECT
            p.match_code,
            p.player_id,
            t.updated_at
        FROM all_players p
        JOIN all_timestamps t
        ON p.match_code = t.match_code
    ),
    score_history AS (
        SELECT
            match_code,
            player_id,
            updated_at,
            point_score,
            match_name
        FROM record_player
    ),
    merged_series AS (
        SELECT
            ts.match_code,
            ts.player_id,
            ts.updated_at,
            sh.point_score,
            sh.match_name
        FROM time_series ts
        LEFT JOIN score_history sh
        ON ts.match_code = sh.match_code
        AND ts.player_id = sh.player_id
        AND ts.updated_at = sh.updated_at
    ),
    filled_series AS (
        SELECT
            match_code,
            player_id,
            updated_at,
            COALESCE(
                MAX(point_score) FILTER (WHERE point_score IS NOT NULL) OVER (
                    PARTITION BY match_code, player_id
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
        p.player_name,
        fs.point_score
    FROM filled_series fs
    JOIN player p ON fs.player_id = p.id
    ORDER BY fs.match_code, fs.player_id, fs.updated_at;
"""



GET_PLAYER_RECORDS_BY_ID_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code FROM record_player
    ),
    all_players AS (
        SELECT DISTINCT player_id, match_code FROM record_player
    ),
    time_series AS (
        SELECT
            p.match_code,
            p.player_id,
            t.updated_at
        FROM all_players p
        JOIN all_timestamps t
        ON p.match_code = t.match_code
    ),
    score_history AS (
        SELECT
            match_code,
            player_id,
            updated_at,
            point_score,
            match_name
        FROM record_player
    ),
    merged_series AS (
        SELECT
            ts.match_code,
            ts.player_id,
            ts.updated_at,
            sh.point_score,
            sh.match_name
        FROM time_series ts
        LEFT JOIN score_history sh
        ON ts.match_code = sh.match_code
        AND ts.player_id = sh.player_id
        AND ts.updated_at = sh.updated_at
    ),
    filled_series AS (
        SELECT
            match_code,
            player_id,
            updated_at,
            COALESCE(
                MAX(point_score) FILTER (WHERE point_score IS NOT NULL) OVER (
                    PARTITION BY match_code, player_id
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
        p.player_name,
        fs.point_score
    FROM filled_series fs
    JOIN player p ON fs.player_id = p.id
    WHERE p.id = :id
    ORDER BY fs.match_code, fs.player_id, fs.updated_at;
"""



GET_PLAYER_RECORDS_BY_MATCH_CODE_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code FROM record_player
    ),
    all_players AS (
        SELECT DISTINCT player_id, match_code FROM record_player
    ),
    time_series AS (
        SELECT
            p.match_code,
            p.player_id,
            t.updated_at
        FROM all_players p
        JOIN all_timestamps t
        ON p.match_code = t.match_code
    ),
    score_history AS (
        SELECT
            match_code,
            player_id,
            updated_at,
            point_score,
            match_name
        FROM record_player
    ),
    merged_series AS (
        SELECT
            ts.match_code,
            ts.player_id,
            ts.updated_at,
            sh.point_score,
            sh.match_name
        FROM time_series ts
        LEFT JOIN score_history sh
        ON ts.match_code = sh.match_code
        AND ts.player_id = sh.player_id
        AND ts.updated_at = sh.updated_at
    ),
    filled_series AS (
        SELECT
            match_code,
            player_id,
            updated_at,
            COALESCE(
                MAX(point_score) FILTER (WHERE point_score IS NOT NULL) OVER (
                    PARTITION BY match_code, player_id
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
        p.player_name,
        fs.point_score
    FROM filled_series fs
    JOIN player p ON fs.player_id = p.id
    WHERE fs.match_code = :match_code
    ORDER BY fs.match_code, fs.player_id, fs.updated_at;
"""