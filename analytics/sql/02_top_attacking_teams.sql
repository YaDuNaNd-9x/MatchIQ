SELECT t.name AS team,
       COUNT(*) AS matches_played,
       SUM(tm.goals_for) AS total_goals,
       ROUND(AVG(tm.goals_for), 2) AS goals_per_match
FROM (
    SELECT home_team_id AS team_id, home_goals AS goals_for
    FROM matches
    UNION ALL
    SELECT away_team_id, away_goals
    FROM matches
) tm
JOIN teams t ON t.id = tm.team_id
GROUP BY t.id, t.name
ORDER BY total_goals DESC
LIMIT 10;