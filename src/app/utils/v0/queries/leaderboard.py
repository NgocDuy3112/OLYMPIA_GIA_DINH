YELLOW_LEADERBOARD_QUERY = """
    WITH latest_records AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    latest_team_scores AS (
        SELECT DISTINCT ON (rt.team_id, rt.match_name)
            rt.team_id,
            rt.match_name,
            rt.point_score
        FROM record_team AS rt
        ORDER BY rt.team_id, rt.match_name, rt.updated_at DESC
    ),
    team_points_per_player AS (
        SELECT 
            p.id AS player_id,
            SUM(lts.point_score) AS team_points
        FROM player AS p
        JOIN latest_team_scores AS lts ON p.team_id = lts.team_id
        GROUP BY p.id
    ),
    bonus_aggregated AS (
        SELECT player_id, SUM(point_score) AS bonus_points
        FROM bonus
        GROUP BY player_id
    )
    SELECT
        p.player_name,
        COALESCE(SUM(lr.point_score), 0) AS player_points,
        COALESCE(tpp.team_points, 0) AS team_points,
        COALESCE(SUM(lr.point_score), 0) + COALESCE(tpp.team_points, 0) AS total_points,
        COALESCE(bonus_aggregated.bonus_points, 0) AS bonus_points
    FROM player AS p
    LEFT JOIN latest_records AS lr ON lr.player_id = p.id
    LEFT JOIN team_points_per_player AS tpp ON tpp.player_id = p.id
    LEFT JOIN bonus_aggregated ON bonus_aggregated.player_id = p.id
    WHERE p.is_dnf = FALSE
    GROUP BY p.id, p.player_name, tpp.team_points, bonus_aggregated.bonus_points
    ORDER BY 
        total_points DESC, 
        bonus_points DESC;
"""


WHITE_LEADERBOARD_QUERY = """
    WITH latest_records AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    latest_team_scores AS (
        SELECT DISTINCT ON (rt.team_id, rt.match_name)
            rt.team_id,
            rt.match_name,
            rt.point_score
        FROM record_team AS rt
        ORDER BY rt.team_id, rt.match_name, rt.updated_at DESC
    ),
    team_points_per_player AS (
        SELECT 
            p.id AS player_id,
            SUM(lts.point_score) AS team_points
        FROM player AS p
        JOIN latest_team_scores AS lts ON p.team_id = lts.team_id
        GROUP BY p.id
    ),
    bonus_aggregated AS (
        SELECT player_id, SUM(point_score) AS bonus_points
        FROM bonus
        GROUP BY player_id
    )
    SELECT
        p.player_name,
        COALESCE(SUM(lr.point_score), 0) AS player_points,
        COALESCE(tpp.team_points, 0) AS team_points,
        COALESCE(SUM(lr.point_score), 0) + COALESCE(tpp.team_points, 0) AS total_points,
        COALESCE(bonus_aggregated.bonus_points, 0) AS bonus_points
    FROM player AS p
    LEFT JOIN latest_records AS lr ON lr.player_id = p.id
    LEFT JOIN team_points_per_player AS tpp ON tpp.player_id = p.id
    LEFT JOIN bonus_aggregated ON bonus_aggregated.player_id = p.id
    WHERE p.is_dnf = FALSE AND p.birth_year >= 2006
    GROUP BY p.id, p.player_name, tpp.team_points, bonus_aggregated.bonus_points
    ORDER BY 
        total_points DESC, 
        bonus_points DESC;
"""


RED_LEADERBOARD_QUERY = """
    WITH latest_records AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    latest_team_scores AS (
        SELECT DISTINCT ON (rt.team_id, rt.match_name)
            rt.team_id,
            rt.match_name,
            rt.point_score
        FROM record_team AS rt
        ORDER BY rt.team_id, rt.match_name, rt.updated_at DESC
    ),
    team_points_per_player AS (
        SELECT 
            p.id AS player_id,
            SUM(lts.point_score) AS team_points
        FROM player AS p
        JOIN latest_team_scores AS lts ON p.team_id = lts.team_id
        GROUP BY p.id
    ),
    bonus_aggregated AS (
        SELECT player_id, SUM(point_score) AS bonus_points
        FROM bonus
        GROUP BY player_id
    )
    SELECT
        p.player_name,
        COALESCE(SUM(lr.point_score), 0) AS player_points,
        COALESCE(tpp.team_points, 0) AS team_points,
        COALESCE(SUM(lr.point_score), 0) + COALESCE(tpp.team_points, 0) AS total_points,
        COALESCE(bonus_aggregated.bonus_points, 0) AS bonus_points
    FROM player AS p
    LEFT JOIN latest_records AS lr ON lr.player_id = p.id
    LEFT JOIN team_points_per_player AS tpp ON tpp.player_id = p.id
    LEFT JOIN bonus_aggregated ON bonus_aggregated.player_id = p.id
    WHERE p.is_dnf = FALSE AND p.player_code IN ('GLO_01', 'GLO_07', 'GLO_08')
    GROUP BY p.id, p.player_name, tpp.team_points, bonus_aggregated.bonus_points
    ORDER BY 
        total_points DESC, 
        bonus_points DESC;
"""


BLUE_LEADERBOARD_QUERY = """
    WITH latest_points AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    bonus_aggregated AS (
        SELECT
            b.player_id,
            SUM(b.point_score) AS bonus_points,
            SUM(b.g_score) AS total_g
        FROM bonus AS b
        GROUP BY b.player_id
    )
    SELECT
        p.player_name,
        COALESCE(SUM(lp.point_score), 0) AS total_points,
        COALESCE(ba.bonus_points, 0) AS bonus_points,
        COALESCE(ba.total_g, 0) AS total_g
    FROM player AS p
    LEFT JOIN latest_points AS lp ON lp.player_id = p.id
    LEFT JOIN bonus_aggregated AS ba ON ba.player_id = p.id
    WHERE p.is_dnf = FALSE
    GROUP BY p.id, p.player_name, ba.bonus_points, ba.total_g
    ORDER BY total_g DESC, total_points DESC, bonus_points DESC;
"""


ORANGE_LEADERBOARD_QUERY = """
    WITH latest_points AS (
        SELECT DISTINCT ON (r.player_id, r.match_name)
            r.player_id,
            r.match_name,
            r.point_score
        FROM record_player AS r
        ORDER BY r.player_id, r.match_name, r.updated_at DESC
    ),
    bonus_aggregated AS (
        SELECT
            b.player_id,
            SUM(b.point_score) AS bonus_points,
            SUM(b.d_score) AS total_d
        FROM bonus AS b
        GROUP BY b.player_id
    )
    SELECT
        p.player_name,
        COALESCE(SUM(lp.point_score), 0) AS total_points,
        COALESCE(ba.bonus_points, 0) AS bonus_points,
        COALESCE(ba.total_d, 0) AS total_d
    FROM player AS p
    LEFT JOIN latest_points AS lp ON lp.player_id = p.id
    LEFT JOIN bonus_aggregated AS ba ON ba.player_id = p.id
    WHERE p.is_dnf = FALSE
    GROUP BY 
        p.id, 
        p.player_name, 
        ba.bonus_points, 
        ba.total_d
    ORDER BY 
        total_d DESC, 
        total_points DESC, 
        bonus_points DESC;
"""


GREEN_LEADERBOARD_QUERY = """
    WITH ranked_changes AS (
        SELECT
            player_id,
            match_name,
            point_score,
            LAG(point_score) OVER (
                PARTITION BY player_id, match_name
                ORDER BY updated_at
            ) AS prev_score
        FROM record_player
    ),
    increases AS (
        SELECT
            player_id,
            match_name,
            CASE 
                WHEN prev_score IS NULL AND point_score > 0 THEN 1
                WHEN point_score > COALESCE(prev_score, 0) THEN 1
                ELSE 0
            END AS increased
        FROM ranked_changes
    ),
    match_bonus AS (
        SELECT
            player_id,
            match_name,
            MAX(increased) AS had_increase
        FROM increases
        GROUP BY player_id, match_name
    ),
    total_increases_per_player AS (
        SELECT
            i.player_id,
            SUM(i.increased) AS raw_increases,
            COUNT(DISTINCT m.match_name) AS matches_with_increase
        FROM increases i
        JOIN match_bonus m 
            ON i.player_id = m.player_id 
        AND i.match_name = m.match_name 
        AND m.had_increase = 1
        GROUP BY i.player_id
    ),
    latest_per_match AS (
        SELECT DISTINCT ON (player_id, match_name)
            player_id,
            match_name,
            point_score
        FROM record_player
        ORDER BY player_id, match_name, updated_at DESC
    ),
    total_points_per_player AS (
        SELECT
            player_id,
            SUM(point_score) AS total_points
        FROM latest_per_match
        GROUP BY player_id
    ),
    bonus_aggregated AS (
        SELECT player_id, SUM(point_score) AS bonus_points
        FROM bonus
        GROUP BY player_id
    )
    SELECT
        p.player_name,
        COALESCE(tp.total_points, 0) AS total_points,
        COALESCE(b.bonus_points, 0) AS bonus_points,
        COALESCE(i.raw_increases, 0) + COALESCE(i.matches_with_increase, 0) AS total_correct_answers
    FROM player AS p
    LEFT JOIN total_points_per_player AS tp ON tp.player_id = p.id
    LEFT JOIN bonus_aggregated AS b ON b.player_id = p.id
    LEFT JOIN total_increases_per_player AS i ON i.player_id = p.id
    ORDER BY
        total_correct_answers DESC,
        total_points DESC,
        bonus_points DESC,
        is_dnf ASC;
"""


PINK_LEADERBOARD_QUERY = """
    WITH latest_per_match AS (
        SELECT DISTINCT ON (player_id, match_code)
            player_id,
            match_code,
            point_score
        FROM record_player
        ORDER BY player_id, match_code, updated_at DESC
    ),
    max_of_latest AS (
        SELECT
            player_id,
            MAX(point_score) AS max_points
        FROM latest_per_match
        GROUP BY player_id
    )
    SELECT
        p.player_name AS player_name,
        m.player_id,
        m.max_points AS max_points
    FROM max_of_latest AS m
    JOIN player AS p ON p.id = m.player_id
    ORDER BY 
        m.max_points DESC,
        is_dnf;
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
    ),
    bonus_points AS (
        SELECT
            p.team_id,
            SUM(b.point_score) AS total_bonus_points
        FROM bonus AS b
        JOIN player AS p ON b.player_id = p.id
        GROUP BY p.team_id
    )
    SELECT
        COALESCE(pp.team_name, tp.team_name) AS team_name,
        COALESCE(pp.total_players_points, 0) AS total_players_points,
        COALESCE(tp.total_team_points, 0) AS total_team_points,
        COALESCE(bp.total_bonus_points, 0) AS total_bonus_points,
        COALESCE(pp.total_players_points, 0) +
        COALESCE(tp.total_team_points, 0) +
        COALESCE(bp.total_bonus_points, 0) AS total_points
    FROM players_points AS pp
    FULL OUTER JOIN team_points AS tp ON pp.team_id = tp.team_id
    FULL OUTER JOIN bonus_points AS bp ON COALESCE(pp.team_id, tp.team_id) = bp.team_id
    ORDER BY total_points DESC;
"""