SELECT s.name AS season,
       COUNT(*) AS total_matches,
       COUNT(*) FILTER (WHERE m.result = 'H') AS home_wins,
       COUNT(*) FILTER (WHERE m.result = 'D') AS draws,
       COUNT(*) FILTER (WHERE m.result = 'A') AS away_wins,
       ROUND(
           100.0 * COUNT(*) FILTER (WHERE m.result = 'H') / COUNT(*), 2
       ) AS home_win_percentage,
       ROUND(
           100.0 * COUNT(*) FILTER (WHERE m.result = 'A') / COUNT(*), 2
       ) AS away_win_percentage
FROM matches m
JOIN seasons s ON s.id = m.season_id
GROUP BY s.id, s.name
ORDER BY s.name;