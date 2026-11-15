from rest_framework import generics
from .models import Competition, Season
from .serializers import CompetitionSerializer, SeasonSerializer


class CompetitionListView(generics.ListAPIView):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer


class SeasonListView(generics.ListAPIView):
    queryset = Season.objects.select_related("competition").all()
    serializer_class = SeasonSerializer