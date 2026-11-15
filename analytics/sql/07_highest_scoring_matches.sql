SELECT s.name AS season,
       m.match_date,
       ht.name AS home_team,
       m.home_goals,
       at.name AS away_team,
       m.away_goals,
       m.total_goals,
       m.result
FROM matches m
JOIN seasons s ON s.id = m.season_id
JOIN teams ht ON ht.id = m.home_team_id
JOIN teams at ON at.id = m.away_team_id
ORDER BY m.total_goals DESC, m.match_date DESC
LIMIT 15;