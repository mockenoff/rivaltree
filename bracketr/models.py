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

from account import models as account_models

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

class Bracket(models.Model):
	""" Bracket model

	"""

	def header_path(self, filename):
		""" Return the header's upload path

		:param filename: Filename uploaded with
		:type filename: str
		:returns: str

		"""
		return 'brackets/%s.%s' % (uuid.uuid1(), get_extension(filename))

	# Structuring metas
	as_json = models.TextField(blank=True)
	has_third_place = models.BooleanField(default=False)
	is_double_elimination = models.BooleanField(default=True)
	is_finished = models.BooleanField(default=False)

	# Display metas
	title = models.CharField(max_length=255, db_index=True)
	header_image = models.ImageField(upload_to=header_path)
	description = models.TextField(blank=True)
	datetime = models.DateTimeField(db_index=True)

	# Object metas
	manager = models.ForeignKey(account_models.Manager, db_index=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Game(models.Model):
	""" Game model
		Flows as bracket > group > round_number > number

	"""

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
	round_number = models.PositiveSmallIntegerField(default=0)
	group = models.PositiveSmallIntegerField(choices=GROUP_CHOICES, default=GROUP_WINNER)
	number = models.PositiveSmallIntegerField(default=0)
	bracket = models.ForeignKey(Bracket, db_index=True)

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

class Team(models.Model):
	""" Team model

	"""

	def header_path(self, filename):
		""" Return the header's upload path

		:param filename: Filename uploaded with
		:type filename: str
		:returns: str

		"""
		return 'teams/%s.%s' % (uuid.uuid1(), get_extension(filename))

	# Display metas
	name = models.CharField(max_length=255)
	win = models.PositiveSmallIntegerField(default=0)
	loss = models.PositiveSmallIntegerField(default=0)
	header_path = models.ImageField(upload_to=header_path)
	bracket = models.ForeignKey(Bracket, db_index=True)

	# Object metas
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
