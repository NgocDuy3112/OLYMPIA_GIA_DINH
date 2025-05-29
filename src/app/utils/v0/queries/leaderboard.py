YELLOW_LEADERBOARD_QUERY = """
    SELECT
        p.player_name AS player_name,
        COALESCE(SUM(latest.point_score), 0) AS total_points,
        COALESCE(SUM(b.point_score), 0) AS bonus_points
    FROM
        player AS p
    LEFT JOIN (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ) AS latest ON latest.player_id = p.id
    LEFT JOIN bonus AS b ON b.player_id = p.id
    WHERE
        p.is_dnf = FALSE
    GROUP BY
        p.id
    ORDER BY
        total_points DESC,
        bonus_points DESC
"""


WHITE_LEADERBOARD_QUERY = """
    SELECT
        p.player_name AS player_name,
        COALESCE(SUM(latest.point_score), 0) AS total_points,
        COALESCE(SUM(b.point_score), 0) AS bonus_points
    FROM
        player AS p
    LEFT JOIN (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ) AS latest ON latest.player_id = p.id
    LEFT JOIN bonus AS b ON b.player_id = p.id
    WHERE
        p.is_dnf = FALSE
        AND p.birth_year >= 2006
    GROUP BY
        p.id
    ORDER BY
        total_points DESC,
        bonus_points DESC
"""


RED_LEADERBOARD_QUERY = """
    SELECT
        p.player_name AS player_name,
        COALESCE(SUM(latest.point_score), 0) AS total_points,
        COALESCE(SUM(b.point_score), 0) AS bonus_points
    FROM
        player AS p
    LEFT JOIN (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ) AS latest ON latest.player_id = p.id
    LEFT JOIN bonus AS b ON b.player_id = p.id
    WHERE
        p.is_dnf = FALSE
        AND p.player_code IN ('GLO_01', 'GLO_07', 'GLO_08')
    GROUP BY
        p.id
    ORDER BY
        total_points DESC,
        bonus_points DESC
"""


PINK_LEADERBOARD_QUERY = """
    SELECT
        p.player_name AS player_name,
        r.player_id,
        MAX(player_match_max.max_points) AS max_points
    FROM (
        SELECT
            player_id,
            match_code,
            MAX(point_score) AS max_points
        FROM record_player
        GROUP BY player_id, match_code
    ) AS player_match_max
    JOIN player p ON p.id = player_match_max.player_id
    JOIN record_player r ON r.player_id = player_match_max.player_id
    GROUP BY p.player_name, r.player_id;
"""


BLUE_LEADERBOARD_QUERY = """
    SELECT
        p.player_name AS player_name,
        COALESCE(SUM(latest.point_score), 0) AS total_points,
        COALESCE(SUM(b.point_score), 0) AS bonus_points,
        COALESCE(SUM(b.g_score), 0) AS total_g
    FROM
        player AS p
    LEFT JOIN (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ) AS latest ON latest.player_id = p.id
    LEFT JOIN bonus AS b ON b.player_id = p.id
    WHERE p.is_dnf = FALSE
    GROUP BY p.id, p.player_name
    ORDER BY
        total_g DESC,
        total_points DESC,
        bonus_points DESC
"""


ORANGE_LEADERBOARD_QUERY = """
    SELECT
        p.player_name AS player_name,
        COALESCE(SUM(latest.point_score), 0) AS total_points,
        COALESCE(SUM(b.point_score), 0) AS bonus_points,
        COALESCE(SUM(b.d_score), 0) AS total_d
    FROM
        player AS p
    LEFT JOIN (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ) AS latest ON latest.player_id = p.id
    LEFT JOIN bonus AS b ON b.player_id = p.id
    WHERE p.is_dnf = FALSE
    GROUP BY p.id, p.player_name
    ORDER BY
        total_d DESC,
        total_points DESC,
        bonus_points DESC
"""


GREEN_LEADERBOARD_QUERY = """
    WITH latest_points AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    ranked_records AS (
        SELECT
            r.player_id,
            r.match_name,
            r.point_score,
            LAG(r.point_score) OVER (
                PARTITION BY r.player_id, r.match_name
                ORDER BY r.updated_at
            ) AS prev_score
        FROM record_player AS r
    ),
    score_increases AS (
        SELECT
            player_id,
            CASE 
                WHEN point_score > COALESCE(prev_score, 0) THEN 1
                ELSE 0
            END AS increased
        FROM ranked_records
    ),
    aggregated AS (
        SELECT
            p.id AS player_id,
            p.player_name,
            p.is_dnf,
            COALESCE(SUM(lp.point_score), 0) AS total_points,
            COALESCE(SUM(b.point_score), 0) AS bonus_points,
            COALESCE(SUM(si.increased), 0) AS total_increases
        FROM player AS p
        LEFT JOIN latest_points AS lp ON lp.player_id = p.id
        LEFT JOIN bonus AS b ON b.player_id = p.id
        LEFT JOIN score_increases AS si ON si.player_id = p.id
        GROUP BY p.id, p.player_name, p.is_dnf
    )
    SELECT *
    FROM aggregated
    ORDER BY
        total_increases DESC,
        total_points DESC,
        bonus_points DESC,
        is_dnf ASC;  -- False (0) first, then True (1)
"""


TEAM_LEADERBOARD_QUERY = """
    WITH latest_player_points AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            p.team_id,
            r.point_score
        FROM record_player AS r
        JOIN player AS p ON r.player_id = p.id
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    players_points AS (
        SELECT
            t.id AS team_id,
            t.team_name AS team_name,
            SUM(lp.point_score) AS total_players_points
        FROM latest_player_points AS lp
        JOIN team AS t ON lp.team_id = t.id
        GROUP BY t.id, t.team_name
    ),
    latest_team_points AS (
        SELECT DISTINCT ON (r.team_id, r.match_name)
            r.team_id,
            r.point_score
        FROM record_team AS r
        ORDER BY r.team_id, r.match_name, r.updated_at DESC
    ),
    team_points AS (
        SELECT
            t.id AS team_id,
            t.team_name AS team_name,
            SUM(ltp.point_score) AS total_team_points
        FROM latest_team_points AS ltp
        JOIN team AS t ON ltp.team_id = t.id
        GROUP BY t.id, t.team_name
    )
    SELECT
        COALESCE(pp.team_name, tp.team_name) AS team_name,
        COALESCE(pp.total_players_points, 0) AS total_players_points,
        COALESCE(tp.total_team_points, 0) AS total_team_points,
        COALESCE(pp.total_players_points, 0) + COALESCE(tp.total_team_points, 0) AS total_points
    FROM players_points AS pp
    FULL OUTER JOIN team_points AS tp ON pp.team_id = tp.team_id
    ORDER BY total_points DESC;
"""