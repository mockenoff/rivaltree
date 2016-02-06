"""
.. module:: models
   :platform: Unix
   :synopsis: Contains the models for the bracketr app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import re
import uuid
import datetime
import simplejson as json
from collections import defaultdict

from django.db import models

from apps.account import models as account_models

def get_extension(filename):
	""" Return the extension to a file

	:param filename: Filename to get the extension from
	:type filename: str
	:returns: str

	"""
	if not isinstance(filename, str):
		raise TypeError('Filename must be a string: %s' % type(filename))
	try:
		return re.search(r'\.([a-zA-Z]+)$', filename).group(0)[1:].lower()
	except Exception as err:
		raise ValueError('Could not find an extension in the filename: %s' % err)

def make_path(instance, filename):
	""" Determine what path to store a file

	:param instance: Class instance
	:type instance: Object
	:param filename: Filename to craft a path for
	:type filename: str
	:returns: str

	"""
	return '%s/%s.%s' % (type(instance).__name__.lower(), uuid.uuid1(), get_extension(filename))

class Bracket(models.Model):
	""" Bracket model

	"""

	def __str__(self):
		""" String representation

		"""
		return '%s (%s) - %s' % (self.title, 'Finished' if self.is_finished else 'Ongoing', self.datetime)

	# Structuring metas
	as_json = models.TextField(blank=True)
	has_third_place = models.BooleanField(default=False)
	is_double_elimination = models.BooleanField(default=True)
	is_finished = models.BooleanField(default=False)

	# Display metas
	title = models.CharField(max_length=255, db_index=True)
	header_image = models.ImageField(upload_to=make_path, blank=True)
	description = models.TextField(blank=True)
	datetime = models.DateTimeField(db_index=True)

	# Object metas
	manager = models.ForeignKey(account_models.Manager, db_index=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Team(models.Model):
	""" Team model

	"""

	def __str__(self):
		""" String representation

		"""
		return '%s (%s - %s) - %s' % (self.name, self.win, self.loss, self.bracket.title)

	# Display metas
	name = models.CharField(max_length=255)
	win = models.PositiveSmallIntegerField(default=0)
	loss = models.PositiveSmallIntegerField(default=0)
	header_path = models.ImageField(upload_to=make_path, blank=True)
	bracket = models.ForeignKey(Bracket, db_index=True)

	# Object metas
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Game(models.Model):
	""" Game model
		Flows as bracket > group > round_number > number

	"""

	def __str__(self):
		""" String representation

		"""
		return '%s - %s - %s - %s (%s:%s v %s:%s)' % (
			self.bracket.title, self.get_group_display(), self.round_number, self.number,
			self.team1.name, self.team1_wins, self.team2.name, self.team2_wins)

	GROUP_WINNER = 1
	GROUP_LOSER = 2
	GROUP_THIRD = 3
	GROUP_ROBIN = 4
	GROUP_WINLOSE = 5
	GROUP_CHOICES = (
		(GROUP_WINNER, 'Winner',),
		(GROUP_LOSER, 'Loser',),
		(GROUP_THIRD, 'Third',),
		(GROUP_ROBIN, 'Round-robin'),
		(GROUP_WINLOSE, 'Winner-loser'),
	)

	# Game metas per bracket
	bracket = models.ForeignKey(Bracket, db_index=True)
	group = models.PositiveSmallIntegerField(choices=GROUP_CHOICES, default=GROUP_WINNER)
	round_number = models.PositiveSmallIntegerField(default=0)
	number = models.PositiveSmallIntegerField(default=0)

	# Team stats per game
	team1 = models.ForeignKey(Team, blank=True, null=True, related_name='+')
	team2 = models.ForeignKey(Team, blank=True, null=True, related_name='+')
	team1_wins = models.PositiveSmallIntegerField(default=0)
	team2_wins = models.PositiveSmallIntegerField(default=0)
	team1_seed = models.PositiveSmallIntegerField(blank=True, null=True)
	team2_seed = models.PositiveSmallIntegerField(blank=True, null=True)

	# Object metas
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

	unique_together = (('bracket', 'group', 'round_number', 'number',),)
