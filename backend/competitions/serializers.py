from rest_framework import serializers
from .models import Competition, Season


class CompetitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Competition
        fields = ["id", "name", "country"]


class SeasonSerializer(serializers.ModelSerializer):
    competition_name = serializers.CharField(
        source="competition.name", read_only=True
    )

    class Meta:
        model = Season
        fields = [
            "id",
            "name",
            "competition",
            "competition_name",
            "start_date",
            "end_date",
        ]