SELECT t.name AS team,
       COUNT(*) AS matches_played,
       SUM(tm.goals_against) AS goals_conceded,
       ROUND(AVG(tm.goals_against), 2) AS conceded_per_match
FROM (
    SELECT home_team_id AS team_id, away_goals AS goals_against
    FROM matches
    UNION ALL
    SELECT away_team_id, home_goals
    FROM matches
) tm
JOIN teams t ON t.id = tm.team_id
GROUP BY t.id, t.name
ORDER BY goals_conceded ASC
LIMIT 10;