from rest_framework import generics
from .models import Match
from .serializers import MatchSerializer


class MatchListView(generics.ListAPIView):
    serializer_class = MatchSerializer

    def get_queryset(self):
        queryset = Match.objects.select_related(
            "season", "home_team", "away_team"
        ).all()

        season = self.request.query_params.get("season")
        team = self.request.query_params.get("team")
        result = self.request.query_params.get("result")

        if season:
            queryset = queryset.filter(season__name=season)

        if team:
            queryset = queryset.filter(
                home_team__name__icontains=team
            ) | queryset.filter(
                away_team__name__icontains=team
            )

        if result in ["H", "D", "A"]:
            queryset = queryset.filter(result=result)

        return queryset.order_by("-match_date")