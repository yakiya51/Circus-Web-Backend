from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from matchqueue.models import Queue 
from matchqueue.serializers import QueueSerializer
from members.models import Member

from permissions import IsAdminOrReadOnly

def walk_players(players):
    in_queue = {
        'Main Tank': [], 'Off Tank': [], 'Main DPS': [], 
        'Flex DPS': [], 'Main Support': [], 'Flex Support': []
    }

    for player in players:
        if player.role == 'Change me':
            continue
        in_queue[player.role].append(player.battle_tag)
    
    print(in_queue)


class QueueViewSet(viewsets.ModelViewSet):
    queryset = Queue.objects.all()
    serializer_class = QueueSerializer
    permission_classes = (IsAdminOrReadOnly,)

    @action(detail=True, methods=['POST'])
    def join_queue(self, request, pk=None):
        queue = Queue.objects.get(id=pk)
        # This is fucking retarded
        # request.user *should* be looking at the Authorization header to auto authenticate.
        # but it's not. war crime.
        instance = Token.objects.get(key=request.headers.get('Authorization').split('Token ')[1])
        queue.players.add(Member.objects.get(id=instance.user_id))

        walk_players(queue.players.all())

        return HttpResponse('Added')
    
    @action(detail=True, methods=['POST'])
    def leave_queue(self, request, pk=None):
        if pk is not None:
            queue = Queue.objects.get(id=pk)
            instance = Token.objects.get(key=request.headers.get('Authorization').split('Token ')[1])
            queue.players.remove(Member.objects.get(id=instance.user_id))
            return Response(data={'removed': True})
        return HttpResponse('<h1>tf u doin</h1>')

    
    @action(detail=True, methods=['GET'])
    def contains(self, request, pk=None):
        in_queue = None

        if pk is not None:
            instance = Token.objects.get(key=request.headers.get('Authorization').split('Token ')[1])
            if Member.objects.get(id=instance.user_id) in Queue.objects.get(id=pk).players.all():
                in_queue = True
            else:
                in_queue = False

        return Response(data={'in_queue': in_queue})