from django.contrib import admin
from django.urls import path, include

from competitions.views import CompetitionListView, SeasonListView
from teams.views import TeamListView
from matches.views import MatchListView


urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/competitions/", CompetitionListView.as_view(), name="competitions"),
    path("api/seasons/", SeasonListView.as_view(), name="seasons"),
    path("api/teams/", TeamListView.as_view(), name="teams"),
    path("api/matches/", MatchListView.as_view(), name="matches"),

    path("api/analytics/", include("analytics.urls")),
    path("api/predictions/", include("predictions.urls")),
]