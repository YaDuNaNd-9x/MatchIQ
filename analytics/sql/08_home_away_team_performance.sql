WITH team_performance AS (
    SELECT home_team_id AS team_id,
           'Home' AS venue,
           COUNT(*) AS played,
           SUM(home_points) AS points,
           SUM(home_goals) AS goals_scored,
           SUM(away_goals) AS goals_conceded
    FROM matches
    GROUP BY home_team_id

    UNION ALL

    SELECT away_team_id,
           'Away',
           COUNT(*),
           SUM(away_points),
           SUM(away_goals),
           SUM(home_goals)
    FROM matches
    GROUP BY away_team_id
)
SELECT t.name AS team, tp.venue,
       tp.played, tp.points,
       ROUND(tp.points::numeric / NULLIF(tp.played, 0), 2) AS points_per_match,
       tp.goals_scored, tp.goals_conceded
FROM team_performance tp
JOIN teams t ON t.id = tp.team_id
ORDER BY t.name, tp.venue;