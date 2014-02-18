from django.db import models
import django.dispatch
from django.dispatch import receiver
from django.core.cache import cache
from uchicagohvz.game.models import *
from uchicagohvz.game.data_apis import *

@receiver(models.signals.post_delete, sender=Kill, dispatch_uid='unzombify')
def unzombify(sender, **kwargs):
	victim = kwargs['instance'].victim
	if not Kill.objects.filter(victim=victim).exists():
		# don't unzombify if Kills with this victim still exist
		victim.human = True
		victim.save()

score_update_required = django.dispatch.Signal(providing_args=['game'])

@receiver(score_update_required)
def refresh_cached_data(sender, **kwargs):
	"""
	needs to be called whenever leaderboards (can) change:
		Add/edit/delete Kill
		Add/edit/delete Squad / edit Player's Squad
		Add/edit/delete Award
		Add/edit/delete HVT, HVD
	"""
	game = kwargs['instance'].game
	keys = ('survival_by_dorm', 'top_humans', 'top_zombies', 
		'most_courageous_dorms', 'most_infectious_dorms', 'humans_per_hour', 
		'kills_by_tod', 'humans_by_major', 'zombies_by_major'
	)
	g = globals()
	# regenerate 
	for fn in keys:
		g[fn](game, use_cache=False)

def kill_changed(sender, **kwargs):
	score_update_required.send(sender=sender, game=kwargs['instance'].killer.game)

models.signals.post_save.connect(kill_changed, sender=Kill, dispatch_uid='kill_save')
models.signals.post_delete.connect(kill_changed, sender=Kill, dispatch_uid='kill_deleted')

def player_changed(sender, **kwargs):
	new_player = kwargs['instance']
	if new_player.active: # force subscription to zombies listhost for all active players
		new_player.profile.subscribe_zombies_listhost = True
		new_player.profile.save()
	try:
		old_player = Player.objects.get(pk=instance.pk)
	except sender.DoesNotExist:
		score_update_required.send(sender=sender, game=new_player.game)
	else:
		if old_player.squad != new_player.squad:
			score_update_required.send(sender=sender, game=new_player.game)
		if new_player.game.status == 'in_progress':
			# TODO: call celery task for human/zombie switching in chat
			if old_player.human == True and new_player.human == False:
				pass
			elif old_player.human == False and new_player.human == True:
				pass

models.signals.pre_save.connect(player_changed, sender=Player, dispatch_uid='player_save') 
models.signals.post_delete.connect(player_changed, sender=Player, dispatch_uid='player_deleted')

def award_changed(sender, **kwargs):
	score_update_required.send(sender=sender, game=kwargs['instance'].game)

models.signals.post_save.connect(award_changed, sender=Award, dispatch_uid='award_saved')
models.signals.m2m_changed.connect(award_changed, sender=Award.players.through, dispatch_uid='award_m2m_changed')
models.signals.post_delete.connect(award_changed, sender=Award, dispatch_uid='award_deleted')

def hvd_changed(sender, **kwargs):
	score_update_required.send(sender=sender, game=kwargs['instance'].game)	

models.signals.post_save.connect(hvd_changed, sender=HighValueDorm, dispatch_uid='hvd_saved')
models.signals.post_delete.connect(hvd_changed, sender=HighValueDorm, dispatch_uid='hvd_deleted')

def hvt_changed(sender, **kwargs):
	score_update_required.send(sender=sender, game=kwargs['instance'].player.game)

models.signals.post_save.connect(hvt_changed, sender=HighValueTarget, dispatch_uid='hvt_saved')
models.signals.post_delete.connect(hvt_changed, sender=HighValueTarget, dispatch_uid='hvt_deleted')