WITH team_matches AS (
    SELECT season_id, home_team_id AS team_id,
           home_goals AS goals_for, away_goals AS goals_against,
           home_points AS points, result = 'H' AS won,
           result = 'D' AS drawn, result = 'A' AS lost
    FROM matches

    UNION ALL

    SELECT season_id, away_team_id,
           away_goals, home_goals,
           away_points, result = 'A',
           result = 'D', result = 'H'
    FROM matches
),
standings AS (
    SELECT season_id, team_id,
           COUNT(*) AS played,
           SUM(won::int) AS wins,
           SUM(drawn::int) AS draws,
           SUM(lost::int) AS losses,
           SUM(goals_for) AS goals_for,
           SUM(goals_against) AS goals_against,
           SUM(goals_for - goals_against) AS goal_difference,
           SUM(points) AS points
    FROM team_matches
    GROUP BY season_id, team_id
)
SELECT s.name AS season, t.name AS team,
       st.played, st.wins, st.draws, st.losses,
       st.goals_for, st.goals_against, st.goal_difference,
       st.points,
       RANK() OVER (
           PARTITION BY st.season_id
           ORDER BY st.points DESC, st.goal_difference DESC, st.goals_for DESC
       ) AS position
FROM standings st
JOIN seasons s ON s.id = st.season_id
JOIN teams t ON t.id = st.team_id
ORDER BY s.name, position;