from rest_framework import serializers
from .models import Match


class MatchSerializer(serializers.ModelSerializer):
    season_name = serializers.CharField(
        source="season.name", read_only=True
    )
    home_team_name = serializers.CharField(
        source="home_team.name", read_only=True
    )
    away_team_name = serializers.CharField(
        source="away_team.name", read_only=True
    )
    result_display = serializers.CharField(
        source="get_result_display", read_only=True
    )

    class Meta:
        model = Match
        fields = [
            "id",
            "match_id",
            "season",
            "season_name",
            "round",
            "match_date",
            "home_team",
            "home_team_name",
            "away_team",
            "away_team_name",
            "home_goals",
            "away_goals",
            "total_goals",
            "result",
            "result_display",
            "home_points",
            "away_points",
        ]