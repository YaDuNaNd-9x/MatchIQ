from rest_framework import generics
from .models import Team
from .serializers import TeamSerializer


class TeamListView(generics.ListAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer