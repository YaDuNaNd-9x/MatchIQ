SELECT s.name AS season,
       COUNT(*) AS matches_played,
       SUM(m.home_goals + m.away_goals) AS total_goals,
       ROUND(AVG(m.home_goals + m.away_goals), 2) AS goals_per_match,
       ROUND(AVG(m.home_goals), 2) AS average_home_goals,
       ROUND(AVG(m.away_goals), 2) AS average_away_goals
FROM matches m
JOIN seasons s ON s.id = m.season_id
GROUP BY s.id, s.name
ORDER BY s.name;