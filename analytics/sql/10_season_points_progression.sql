WITH team_season_points AS (
    SELECT season_id, team_id, SUM(points) AS points
    FROM (
        SELECT season_id, home_team_id AS team_id, home_points AS points
        FROM matches
        UNION ALL
        SELECT season_id, away_team_id, away_points
        FROM matches
    ) all_matches
    GROUP BY season_id, team_id
)
SELECT s.name AS season,
       t.name AS team,
       tsp.points,
       LAG(tsp.points) OVER (
           PARTITION BY tsp.team_id
           ORDER BY s.name
       ) AS previous_season_points,
       tsp.points - LAG(tsp.points) OVER (
           PARTITION BY tsp.team_id
           ORDER BY s.name
       ) AS points_change
FROM team_season_points tsp
JOIN seasons s ON s.id = tsp.season_id
JOIN teams t ON t.id = tsp.team_id
ORDER BY t.name, s.name;