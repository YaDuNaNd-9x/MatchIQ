WITH team_matches AS (
    SELECT match_date, season_id, home_team_id AS team_id,
           home_points AS points,
           CASE result WHEN 'H' THEN 'W' WHEN 'D' THEN 'D' ELSE 'L' END AS outcome
    FROM matches

    UNION ALL

    SELECT match_date, season_id, away_team_id,
           away_points,
           CASE result WHEN 'A' THEN 'W' WHEN 'D' THEN 'D' ELSE 'L' END
    FROM matches
),
ranked_matches AS (
    SELECT *,
           ROW_NUMBER() OVER (
               PARTITION BY team_id
               ORDER BY match_date DESC, season_id DESC
           ) AS match_rank
    FROM team_matches
)
SELECT t.name AS team,
       COUNT(*) AS matches_in_sample,
       SUM(rm.points) AS points_last_five,
       STRING_AGG(rm.outcome, ' ' ORDER BY rm.match_rank DESC) AS recent_form
FROM ranked_matches rm
JOIN teams t ON t.id = rm.team_id
WHERE rm.match_rank <= 5
GROUP BY t.id, t.name
ORDER BY points_last_five DESC, t.name;