from django.urls import path
from .views import (
    StandingsView,
    TeamStatsView,
    GoalsBySeasonView,
    ResultDistributionView,
    TopTeamsView,
)

urlpatterns = [
    path("standings/", StandingsView.as_view(), name="standings"),
    path("team-stats/", TeamStatsView.as_view(), name="team-stats"),
    path("goals/", GoalsBySeasonView.as_view(), name="goals"),
    path("results/", ResultDistributionView.as_view(), name="results"),
    path("top-teams/", TopTeamsView.as_view(), name="top-teams"),
]