from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from uchicagohvz.game.models import *
from uchicagohvz.game.data_apis import *
from uchicagohvz.game.serializers import *
from django.utils import timezone

class KillFeed(ListAPIView):
	serializer_class = KillSerializer

	def get_queryset(self):
		game = get_object_or_404(Game, id=self.kwargs['pk'])
		return Kill.objects.exclude(parent=None).filter(victim__game=game).order_by('-date')

class PlayerKillFeed(ListAPIView):
	serializer_class = KillSerializer

	def get_queryset(self):
		player = get_object_or_404(Player, id=self.kwargs['pk'], active=True, human=False)
		return Kill.objects.exclude(parent=None).exclude(victim=player).filter(killer=player)

class SquadKillFeed(ListAPIView):
	serializer_class = KillSerializer
	def get_queryset(self):
		squad = get_object_or_404(Squad, id=self.kwargs['pk'])
		return squad.get_kills()

class HumansPerHour(APIView):
	def get(self, request, *args, **kwargs):
		game = get_object_or_404(Game, id=kwargs['pk'])
		data = humans_per_hour(game)
		return Response(data)

class KillsByTimeOfDay(APIView):
	def get(self, request, *args, **kwargs):
		game = get_object_or_404(Game, id=kwargs['pk'])
		data = kills_by_tod(game)
		return Response(data)

class HumansByMajor(APIView):
	def get(self, request, *args, **kwargs):
		game = get_object_or_404(Game, id=kwargs['pk'])
		data = humans_by_major(game)
		return Response(data)

class ZombiesByMajor(APIView):
	def get(self, request, *args, **kwargs):
		game = get_object_or_404(Game, id=kwargs['pk'])
		data = zombies_by_major(game)
		return Response(data)

class MissionFeed(ListAPIView):
	permission_classes = (IsAuthenticated, )
	serializer_class = MissionSerializer

	def get_queryset(self):
		game_id = self.kwargs['pk']
		user_id = self.request.user.id
		player = get_object_or_404(Player, game__id=game_id, user__id=user_id)
		if not player.active or player.starved or player.suspended:
			raise PermissionDenied
		now = timezone.now()
		# return missions that are currently available (i.e. now is between start date and end date)
		missions = Mission.objects.exclude(start_date__gte=now).filter(end_date__gte=now).filter(game__id=game_id).order_by('end_date')
		if player.human:
			return missions.exclude(def_redeem_type='Z')
		else:
			return missions.exclude(def_redeem_type='H')

class MissionFeedAll(ListAPIView):
	serializer_class = MissionSerializer

	def get_queryset(self):
		game_id = self.kwargs['pk']
		now = timezone.now()
		# return missions that are currently available (i.e. now is between start date and end date)
		return Mission.objects.filter(game__id=game_id).exclude(end_date__gte=now).order_by('end_date')

class Humans(APIView):
	permission_classes = (IsAdminUser, )

	def get(self, request, format=None, *args, **kwargs):
		game_id = self.kwargs['pk']
		players = Player.objects.exclude(active=False).exclude(human=False).filter(game__id=game_id)
		return Response('; '.join([player.user.email for player in players]))

class Zombies(APIView):
	permission_classes = (IsAdminUser, )

	def get(self, request, format=None, *args, **kwargs):
		game_id = self.kwargs['pk']
		players = Player.objects.exclude(active=False).exclude(human=True).filter(game__id=game_id)
		return Response('; '.join([player.user.email for player in players]))

class Players(APIView):
	permission_classes = (IsAdminUser, )

	def get(self, request, format=None, *args, **kwargs):
		game_id = self.kwargs['pk']
		players = Player.objects.exclude(active=False).filter(game__id=game_id)
		return Response('; '.join([player.user.email for player in players]))

class HCommando(APIView):
	permission_classes = (IsAdminUser, )

	def get(self, request, format=None, *args, **kwargs):
		game_id = self.kwargs['pk']
		hvts = HighValueTarget.objects.exclude(player__active=False).filter(player__game__id=game_id)
		return Response('; '.join([hvt.player.user.email for hvt in hvts]))

class ZCommando(APIView):
	permission_classes = (IsAdminUser, )

	def get(self, request, format=None, *args, **kwargs):
		return Response('')

