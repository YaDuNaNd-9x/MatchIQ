from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response


def execute_query(sql, params=None):
    with connection.cursor() as cursor:
        cursor.execute(sql, params or [])
        columns = [column[0] for column in cursor.description]
        return [
            dict(zip(columns, row))
            for row in cursor.fetchall()
        ]


class StandingsView(APIView):
    def get(self, request):
        season = request.query_params.get("season")

        sql = """
            WITH team_matches AS (
                SELECT season_id, home_team_id AS team_id,
                       home_goals AS goals_for,
                       away_goals AS goals_against,
                       home_points AS points,
                       (result = 'H') AS won,
                       (result = 'D') AS drawn,
                       (result = 'A') AS lost
                FROM matches

                UNION ALL

                SELECT season_id, away_team_id,
                       away_goals, home_goals,
                       away_points,
                       (result = 'A'),
                       (result = 'D'),
                       (result = 'H')
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
                   st.goals_for, st.goals_against,
                   st.goal_difference, st.points,
                   RANK() OVER (
                       ORDER BY st.points DESC,
                                st.goal_difference DESC,
                                st.goals_for DESC
                   ) AS position
            FROM standings st
            JOIN seasons s ON s.id = st.season_id
            JOIN teams t ON t.id = st.team_id
            WHERE s.name = COALESCE(
                %s,
                (SELECT MAX(name) FROM seasons)
            )
            ORDER BY position;
        """

        return Response(execute_query(sql, [season]))


class TeamStatsView(APIView):
    def get(self, request):
        sql = """
            WITH team_matches AS (
                SELECT home_team_id AS team_id,
                       home_goals AS goals_for,
                       away_goals AS goals_against,
                       home_points AS points
                FROM matches

                UNION ALL

                SELECT away_team_id,
                       away_goals,
                       home_goals,
                       away_points
                FROM matches
            )
            SELECT t.name AS team,
                   COUNT(*) AS matches_played,
                   SUM(tm.points) AS total_points,
                   SUM(tm.goals_for) AS goals_scored,
                   SUM(tm.goals_against) AS goals_conceded,
                   SUM(tm.goals_for - tm.goals_against) AS goal_difference,
                   ROUND(AVG(tm.points), 2) AS points_per_match
            FROM team_matches tm
            JOIN teams t ON t.id = tm.team_id
            GROUP BY t.id, t.name
            ORDER BY total_points DESC;
        """

        return Response(execute_query(sql))


class GoalsBySeasonView(APIView):
    def get(self, request):
        sql = """
            SELECT s.name AS season,
                   COUNT(*) AS matches_played,
                   SUM(m.home_goals + m.away_goals) AS total_goals,
                   ROUND(
                       AVG(m.home_goals + m.away_goals)::numeric, 2
                   ) AS goals_per_match,
                   ROUND(AVG(m.home_goals)::numeric, 2) AS average_home_goals,
                   ROUND(AVG(m.away_goals)::numeric, 2) AS average_away_goals
            FROM matches m
            JOIN seasons s ON s.id = m.season_id
            GROUP BY s.id, s.name
            ORDER BY s.name;
        """

        return Response(execute_query(sql))


class ResultDistributionView(APIView):
    def get(self, request):
        sql = """
            SELECT
                CASE result
                    WHEN 'H' THEN 'Home Win'
                    WHEN 'D' THEN 'Draw'
                    WHEN 'A' THEN 'Away Win'
                END AS outcome,
                COUNT(*) AS matches,
                ROUND(
                    100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2
                ) AS percentage
            FROM matches
            GROUP BY result
            ORDER BY matches DESC;
        """

        return Response(execute_query(sql))


class TopTeamsView(APIView):
    def get(self, request):
        sql = """
            SELECT t.name AS team,
                   COUNT(*) AS matches_played,
                   SUM(tm.goals_for) AS total_goals,
                   ROUND(AVG(tm.goals_for)::numeric, 2) AS goals_per_match
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
        """

        return Response(execute_query(sql))