GET_PLAYER_RECORDS_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code
        FROM record_player
    ),
    all_players AS (
        SELECT DISTINCT player_id, match_code
        FROM record_player
    ),
    complete_time_grid AS (
        SELECT 
            p.player_id,
            t.match_code,
            t.updated_at
        FROM all_players p
        JOIN all_timestamps t 
        ON p.match_code = t.match_code
    ),
    grid_with_scores AS (
        SELECT 
            ctg.player_id,
            ctg.match_code,
            ctg.updated_at,
            rp.point_score,
            rp.match_name
        FROM complete_time_grid ctg
        LEFT JOIN record_player rp
        ON ctg.player_id = rp.player_id
        AND ctg.match_code = rp.match_code
        AND ctg.updated_at = rp.updated_at
    ),
    -- Use a simple approach: mark where we have values and carry them forward
    marked_values AS (
        SELECT 
            *,
            -- Create groups: each time we have a real value, start a new group
            SUM(CASE WHEN point_score IS NOT NULL THEN 1 ELSE 0 END) 
            OVER (
                PARTITION BY match_code, player_id 
                ORDER BY updated_at 
                ROWS UNBOUNDED PRECEDING
            ) AS value_group
        FROM grid_with_scores
    ),
    filled_scores AS (
        SELECT 
            player_id,
            match_code,
            updated_at,
            point_score AS original_score,
            match_name AS original_match_name,
            value_group,
            -- Within each group, get the first non-null value (which is the value to carry forward)
            MAX(point_score) OVER (
                PARTITION BY match_code, player_id, value_group
            ) AS carried_score,
            MAX(match_name) OVER (
                PARTITION BY match_code, player_id, value_group
            ) AS carried_match_name
        FROM marked_values
        WHERE value_group > 0  -- Only include records where we have at least one actual score
    )
    SELECT
        fs.updated_at,
        fs.carried_match_name AS match_name,
        p.player_name,
        fs.carried_score AS point_score,
        CASE 
            WHEN fs.original_score IS NOT NULL THEN 'ACTUAL'
            ELSE 'FILLED'
        END AS record_type
    FROM filled_scores fs
    JOIN player p ON p.id = fs.player_id
    ORDER BY fs.match_code, fs.player_id, fs.updated_at;
"""



GET_PLAYER_RECORDS_BY_ID_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code
        FROM record_player
    ),
    all_players AS (
        SELECT DISTINCT player_id, match_code
        FROM record_player
    ),
    complete_time_grid AS (
        SELECT 
            p.player_id,
            t.match_code,
            t.updated_at
        FROM all_players p
        JOIN all_timestamps t 
        ON p.match_code = t.match_code
    ),
    grid_with_scores AS (
        SELECT 
            ctg.player_id,
            ctg.match_code,
            ctg.updated_at,
            rp.point_score,
            rp.match_name
        FROM complete_time_grid ctg
        LEFT JOIN record_player rp
        ON ctg.player_id = rp.player_id
        AND ctg.match_code = rp.match_code
        AND ctg.updated_at = rp.updated_at
    ),
    -- Use a simple approach: mark where we have values and carry them forward
    marked_values AS (
        SELECT 
            *,
            -- Create groups: each time we have a real value, start a new group
            SUM(CASE WHEN point_score IS NOT NULL THEN 1 ELSE 0 END) 
            OVER (
                PARTITION BY match_code, player_id 
                ORDER BY updated_at 
                ROWS UNBOUNDED PRECEDING
            ) AS value_group
        FROM grid_with_scores
    ),
    filled_scores AS (
        SELECT 
            player_id,
            match_code,
            updated_at,
            point_score AS original_score,
            match_name AS original_match_name,
            value_group,
            -- Within each group, get the first non-null value (which is the value to carry forward)
            MAX(point_score) OVER (
                PARTITION BY match_code, player_id, value_group
            ) AS carried_score,
            MAX(match_name) OVER (
                PARTITION BY match_code, player_id, value_group
            ) AS carried_match_name
        FROM marked_values
        WHERE value_group > 0  -- Only include records where we have at least one actual score
    )
    SELECT
        fs.updated_at,
        fs.carried_match_name AS match_name,
        p.player_name,
        fs.carried_score AS point_score,
        CASE 
            WHEN fs.original_score IS NOT NULL THEN 'ACTUAL'
            ELSE 'FILLED'
        END AS record_type
    FROM filled_scores fs
    JOIN player p ON p.id = fs.player_id
    WHERE p.id = :id
    ORDER BY fs.match_code, fs.player_id, fs.updated_at;
"""



GET_PLAYER_RECORDS_BY_MATCH_CODE_QUERY = """
    WITH all_timestamps AS (
        SELECT DISTINCT updated_at, match_code
        FROM record_player
    ),
    all_players AS (
        SELECT DISTINCT player_id, match_code
        FROM record_player
    ),
    complete_time_grid AS (
        SELECT 
            p.player_id,
            t.match_code,
            t.updated_at
        FROM all_players p
        JOIN all_timestamps t 
        ON p.match_code = t.match_code
    ),
    grid_with_scores AS (
        SELECT 
            ctg.player_id,
            ctg.match_code,
            ctg.updated_at,
            rp.point_score,
            rp.match_name
        FROM complete_time_grid ctg
        LEFT JOIN record_player rp
        ON ctg.player_id = rp.player_id
        AND ctg.match_code = rp.match_code
        AND ctg.updated_at = rp.updated_at
    ),
    -- Use a simple approach: mark where we have values and carry them forward
    marked_values AS (
        SELECT 
            *,
            -- Create groups: each time we have a real value, start a new group
            SUM(CASE WHEN point_score IS NOT NULL THEN 1 ELSE 0 END) 
            OVER (
                PARTITION BY match_code, player_id 
                ORDER BY updated_at 
                ROWS UNBOUNDED PRECEDING
            ) AS value_group
        FROM grid_with_scores
    ),
    filled_scores AS (
        SELECT 
            player_id,
            match_code,
            updated_at,
            point_score AS original_score,
            match_name AS original_match_name,
            value_group,
            -- Within each group, get the first non-null value (which is the value to carry forward)
            MAX(point_score) OVER (
                PARTITION BY match_code, player_id, value_group
            ) AS carried_score,
            MAX(match_name) OVER (
                PARTITION BY match_code, player_id, value_group
            ) AS carried_match_name
        FROM marked_values
        WHERE value_group > 0  -- Only include records where we have at least one actual score
    )
    SELECT
        fs.updated_at,
        fs.carried_match_name AS match_name,
        p.player_name,
        fs.carried_score AS point_score,
        CASE 
            WHEN fs.original_score IS NOT NULL THEN 'ACTUAL'
            ELSE 'FILLED'
        END AS record_type
    FROM filled_scores fs
    JOIN player p ON p.id = fs.player_id
    WHERE fs.match_code = :match_code
    ORDER BY fs.match_code, fs.player_id, fs.updated_at;
"""