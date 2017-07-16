from rest_framework import serializers
from uchicagohvz.game.models import *

class KillSerializer(serializers.ModelSerializer):
	class Meta:
		model = Kill
		fields = ('id', 'killer', 'victim', 'location', 'date', 'points')

	killer = serializers.SerializerMethodField(method_name='get_killer')
	victim = serializers.SerializerMethodField(method_name='get_victim')
	location = serializers.SerializerMethodField(method_name='get_location')

	def get_killer(self, obj):
		return obj.killer.display_name

	def get_victim(self, obj):
		return obj.victim.display_name

	def get_location(self, obj):
		if not obj.pos:
			return None
		return obj.pos.rsplit(',')

class MissionSerializer(serializers.ModelSerializer):
	class Meta:
		model = Mission
		fields = ('id', 'name', 'end_date', 'img', 'location', 'rtype')

	location = serializers.SerializerMethodField(method_name='get_location')
	rtype = serializers.SerializerMethodField(method_name='get_rtype')

	def get_location(self, obj):
		if not obj.pos:
			return None
		return obj.pos.rsplit(',')

	def get_rtype(self, obj):
		return obj.def_redeem_type
