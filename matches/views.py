from itertools import chain

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from matches.models import Match
from matches.serializers import MatchSerializer


class MatchViewSet(viewsets.ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=False, methods=['GET'])
    def sort(self, request):
        queryset = None

        if 'username' in request.query_params:
            red = Match.objects.filter(red_team__username=request.query_params.get('username'))
            blue = Match.objects.filter(blue_team__username=request.query_params.get('username'))
            queryset = list(chain(red, blue))

        return Response(MatchSerializer(instance=queryset, many=True).data)
