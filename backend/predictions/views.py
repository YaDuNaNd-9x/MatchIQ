from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from teams.models import Team
from .services import predict_match


class MatchPredictionView(APIView):

    def post(self, request):
        home_team_id = request.data.get("home_team_id")
        away_team_id = request.data.get("away_team_id")

        if not home_team_id or not away_team_id:
            return Response(
                {"error": "Both home_team_id and away_team_id are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            home_team = Team.objects.get(id=home_team_id)
            away_team = Team.objects.get(id=away_team_id)

        except Team.DoesNotExist:
            return Response(
                {"error": "One or both teams do not exist."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if home_team.id == away_team.id:
            return Response(
                {"error": "Home and away teams must be different."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            prediction = predict_match(home_team, away_team)

        except FileNotFoundError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        return Response(prediction, status=status.HTTP_200_OK)