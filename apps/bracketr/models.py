"""
.. module:: models
   :platform: Unix
   :synopsis: Contains the models for the bracketr app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import re
import math
import uuid
import datetime
import itertools
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

	@property
	def teams(self):
		""" Property to find all the EventTeam objects for the Division

		:returns: list

		"""
		return list(Team.objects.filter(bracket=self))

	@property
	def games(self):
		""" Property to find all the Game objects and order them by ('group', 'round_number', 'number')

		"""
		return list(Game.objects.filter(bracket=self).order_by('group', 'round_number', 'number'))

	@property
	def first_round(self):
		""" Find the first round of the bracket

		"""
		first_round = 0
		for game in self.games:
			if game.group == Game.GROUP_WINNER and game.round_number > first_round:
				first_round = game.round_number
		return first_round

	@staticmethod
	def is_round_done(games):
		""" Determine if all the games in a round are "done"

		:param games: The games to examine for the round
		:type games: list
		:returns: bool

		"""
		for game in games:
			if not game['team1']['id'] or not game['team2']['id'] or (not game['team1']['wins'] and not game['team2']['wins']):
				return False
		return True

	@staticmethod
	def seed_from_round(seeds, games):
		""" Fill up any existing seeds with new game results

		:param seeds: Matching up seeds to team IDs
		:type seeds: dict
		:param games: Games of the round
		:type games: list
		:returns: dict

		"""
		for game in games:
			# Assume a game is worthwhile if the teams are set (duh) and there are some wins
			if Bracket.is_round_done([game]):
				# Only change the seeding if team2 upsets team1
				if game['team1']['wins'] < game['team2']['wins']:
					seeds[game['team1']['seed']] = game['team2']['id']
					seeds[game['team2']['seed']] = game['team1']['id']
		return seeds

	def make_games(self, clear=False):
		""" Create all the related Game objects (should happen first and only once per teams alteration)

		:param clear: Empty out all the currently existing Game objects
		:type clear: bool

		"""
		if clear:
			Game.objects.filter(bracket=self).delete()

		games = dict()
		teams = self.teams

		games['round_robin'], saves = self.make_round_robin(teams=teams, save=True)
		games['winners'], saves = self.make_bracket(teams=len(teams), group=Game.GROUP_WINNER, save=True)

		if self.is_double_elimination:
			games['losers'], saves = self.make_losers_bracket(games['winners'], save=True)
			games['winner_loser'], saves = self.make_winlose_bracket(save=True)
		elif self.has_third_place:
			games['third'], saves = self.make_bracket(2, group=Game.GROUP_THIRD, save=False)

		return games

	def make_winlose_bracket(self, save=False):
		""" Generate the rounds for the winner/loser clash

		:param save: Whether to save the created Game objects
		:type save: bool
		:returns: dict

		"""
		games = [
			Game(bracket=self, group=Game.GROUP_WINLOSE, round_number=0, number=0, team1_seed=1, team2_seed=2),
			Game(bracket=self, group=Game.GROUP_WINLOSE, round_number=1, number=0, team1_seed=1, team2_seed=2),
		]

		bracket = list()
		for game in games:
			bracket.append([{
				'team1': Game.make_bracket_object(game.team1_seed),
				'team2': Game.make_bracket_object(game.team2_seed),
			}])

		if save:
			Game.objects.bulk_create(games)

		return bracket, games

	def make_bracket(self, teams, group, save=False):
		""" Generate a bracket object

		:param teams: Make blank if teams is an int or will use teams order as seeds
		:type teams: list
		:param group: Bracket group type
		:type group: Game.GROUP_CHOICES
		:param save: Whether to save the created Game objects
		:type save: bool
		:returns: dict

		"""
		try:
			count = len(teams)
		except TypeError:
			count = teams
			teams = None

		games = list()
		bracket = list()
		seeded = set()
		rounds = math.ceil(math.log(count, 2))

		for rnum in range(rounds):
			bracket.append(list())
			game_count = int(math.pow(2, rnum))
			team_count = game_count * 2

			for gnum in range(game_count):
				seed1 = gnum + 1
				seed2 = team_count - (seed1 - 1)

				if seed2 > count:
					continue
				if seed1 > seed2:
					break

				bracket[rnum].append({
					'team1': Game.make_bracket_object(seed1),
					'team2': Game.make_bracket_object(seed2),
				})
				game = Game(bracket=self, group=group, round_number=rnum, number=gnum, team1_seed=seed1, team2_seed=seed2)

				if teams:
					teams1 = teams[seed1-1]
					teams2 = teams[seed2-1]

					if teams1 not in seeded:
						game.team1 = teams[seed1-1]
						game.team1_seed = seed1
						bracket[rnum][gnum]['team1']['id'] = game.team1.id.hex
						seeded.add(game.team1)

					if teams2 not in seeded:
						game.team2 = teams[seed2-1]
						game.team2_seed = seed2
						bracket[rnum][gnum]['team2']['id'] = teams[seed2-1].id.hex
						seeded.add(game.team2)

				games.append(game)

		if save:
			Game.objects.bulk_create(games)

		return bracket, games

	def make_losers_bracket(self, winners, save=False):
		""" Create a losers bracket from a winners bracket
			Turns out there's two phases to this: trim and sustain

		:param winners: Single elimination bracket to build against
		:type winners: dict
		:param save: Whether to save the created Game objects
		:type save: bool
		:returns: dict

		"""
		games = list()
		round_count = len(winners)
		sustain_count = round_count - 1

		bracket = [list() for scount in range(sustain_count * 2)]
		last_seed = winners[-1][0]['team2']['seed']

		sustain = True
		seed_start = 2

		for rnum in range(sustain_count * 2):
			games_number = int(math.pow(2, math.floor(rnum / 2)))

			if not sustain:
				seed_start += games_number

			sustain = not sustain

			if games_number < 2:
				# Special case for the last two rounds
				if seed_start + 1 <= last_seed:
					game = Game(bracket=self, group=Game.GROUP_LOSER, round_number=rnum, number=len(bracket[rnum]), team1_seed=seed_start, team2_seed=(seed_start + 1))
					bracket[rnum].append({
						'team1': Game.make_bracket_object(game.team1_seed),
						'team2': Game.make_bracket_object(game.team2_seed),
					})
					games.append(game)

			elif sustain:
				# Basic pairing in a trimming round
				for snum in range(seed_start, seed_start + games_number):
					bottom_seed = (games_number * 2 * 2) - (snum - seed_start)
					if bottom_seed <= last_seed:
						games.append(Game(bracket=self, group=Game.GROUP_LOSER, round_number=rnum, number=len(bracket[rnum]), team1_seed=snum, team2_seed=bottom_seed))
						bracket[rnum].append({
							'team1': Game.make_bracket_object(snum),
							'team2': Game.make_bracket_object(bottom_seed),
						})

			else:
				# Special pairing in a sustaining round
				for snum in range(seed_start, seed_start + games_number):
					bottom_seed = (seed_start + (games_number * 2)) - (snum - seed_start) - 1
					if bottom_seed <= last_seed:
						games.append(Game(bracket=self, group=Game.GROUP_LOSER, round_number=rnum, number=len(bracket[rnum]), team1_seed=snum, team2_seed=bottom_seed))
						bracket[rnum].append({
							'team1': Game.make_bracket_object(snum),
							'team2': Game.make_bracket_object(bottom_seed),
						})

		if save:
			Game.objects.bulk_create(games)

		return bracket, games

	def make_round_robin(self, teams, save=False):
		""" Create all the round-robin Game objects
			Helpful algorithm page: https://nrich.maths.org/1443

		:param teams: All of the teams
		:type teams: list
		:param save: Whether to save the created Game objects
		:type save: bool
		:returns: list

		"""
		pairs = list(itertools.combinations(teams, 2))

		rnum = 0
		games = list()
		team_total = len(teams)
		oddity = None

		if team_total % 2 == 0:
			team_total -= 1
			oddity = teams.pop()

		bracket = [list() for i in range(team_total)]
		while rnum < team_total:
			number = 0
			midpoint = math.floor(team_total / 2)
			while number < midpoint:
				number += 1
				game = Game(bracket=self, group=Game.GROUP_ROBIN, round_number=rnum, number=number-1, team1=teams[midpoint-number], team2=teams[midpoint+number])
				bracket[rnum].append({
					'team1': Game.make_bracket_object(game.team1),
					'team2': Game.make_bracket_object(game.team2),
				})
				games.append(game)
			if oddity:
				game = Game(bracket=self, group=Game.GROUP_ROBIN, round_number=rnum, number=number, team1=teams[midpoint], team2=oddity)
				bracket[rnum].append({
					'team1': Game.make_bracket_object(game.team1),
					'team2': Game.make_bracket_object(game.team2),
				})
				games.append(game)
			teams.insert(0, teams.pop())
			rnum += 1

		if save:
			Game.objects.bulk_create(games)

		return bracket, games

	def get_game(self, *args, **kwargs):
		""" Get a particular Game object

		:param game_id: ID of the Game object to fetch
		:type game_id: int
		:returns: Game

		"""
		try:
			game_id = kwargs.get('game_id') or args[0]
		except IndexError:
			game_id = None

		if isinstance(game_id, int):
			return Game.objects.get(pk=game_id, bracket=self)

		return Game.objects.get(bracket=self, group=kwargs['group'], round_number=kwargs['round'], number=kwargs['number'])

	def set_game(self, *args, **kwargs):
		""" Set the stats for a game
			Can find the game either by ID or by group > round_number > number

		:param game: Game object to update
		:type game: Game
		:returns: Game

		"""
		game = kwargs.get('game')
		if not isinstance(game, Game):
			game = self.get_game(*args, **kwargs)

		for key, value in kwargs.items():
			if hasattr(game, key) and key not in Game.unique_together:
				setattr(game, key, value)

		if game.pk:
			game.save()

		return game

	def save(self, *args, **kwargs):
		""" Override the save method so it generates the JSON representation

		"""
		if self.pk:
			self.as_json = json.dumps(self.to_dict())

		super(Bracket, self).save(*args, **kwargs)

	def to_dict(self):
		""" Return the bracket formation as a dict
			The goal is to build up the seed dict from saved game results

		:returns: dict

		"""
		teams = self.teams

		bracket = {
			'seeds': {(i + 1): None for i in range(len(teams))},
			'teams': {team.id.hex: {
				'name': team.name,
				'header_path': team.header_path.name,
				'seed': None,
			} for team in teams},
			'winners': [],
			'round_robin': [],
		}

		group_keys = {
			Game.GROUP_WINNER: 'winners',
			Game.GROUP_LOSER: 'losers',
			Game.GROUP_THIRD: 'third',
			Game.GROUP_WINLOSE: 'winner_loser',
			Game.GROUP_ROBIN: 'round_robin',
		}

		if self.is_double_elimination:
			bracket['losers'] = []
			bracket['winner_loser'] = []
		elif self.has_third_place:
			bracket['third'] = []

		results = defaultdict(int)
		for game in self.games:
			if game.group == Game.GROUP_ROBIN:
				results[game.team1_id.hex] += game.team1_wins
				results[game.team2_id.hex] += game.team2_wins

			group_key = group_keys[game.group]
			while len(bracket[group_key]) <= game.round_number:
				bracket[group_key].append(list())
			bracket[group_key][game.round_number].append(game.for_bracket())

		# Sort up total team wins from round-robin
		results = [{'id': key, 'wins': value} for key, value in results.items()]
		results.sort(key=lambda x: x['wins'], reverse=True)
		bracket['seeds'].update({(i + 1): res['id'] for i, res in enumerate(results)})

		# Keep calling seed_from_round() with each round to build up the seeding
		for group in ['winners', 'losers', 'third', 'winner_loser']:
			if group in bracket:
				for games in bracket[group]:
					bracket['seeds'] = Bracket.seed_from_round(bracket['seeds'], games)

		return bracket

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

	@staticmethod
	def make_bracket_object(team=None):
		obj = {'id': None, 'wins': 0, 'seed': None,}
		if isinstance(team, Team):
			obj['id'] = team.id.hex
		elif isinstance(team, int):
			obj['seed'] = team
		return obj

	@property
	def prev(self):
		""" Find the feeder games for a game

		:returns: tuple

		"""
		# Get previous round
			# Check if any of them have matching seeds
			# (Should always stop here if from winners bracket)
		# If not complete
		# (Meaning this is from losers bracket)
			# If sustain
				# Find matching seeds in winners.rounds[math.ceil(math.log(seed, 2))]
			# If trim
				# team1 from winners.round[math.ceil(math.log(seed, 2))]
				# team2 from winners.round[math.ceil(math.log(seed, 2))]
		pass

	@property
	def next(self):
		""" Find the next games this game feeds into

		:returns: Game

		"""
		if self.group == Game.GROUP_WINLOSE:
			# The win-lose rounds are very simple: either the loser wins and it goes to winlose round 0 or stops
			if self.round_number == 1:
				next_game = Game.objects.filter(bracket=self.bracket, group=Game.GROUP_WINLOSE, round_number=0)[0]
				return (next_game, next_game)
			else:
				return (None, None)

		if self.group == Game.GROUP_LOSER:
			# Special optimization for the championship loser game
			if self.round_number == 0:
				return (Game.objects.filter(bracket=self.bracket, group=Game.GROUP_WINLOSE, round_number=1)[0], None)

			# Find the matching team1 seed game in the next round
			match = None
			for game in reversed(self.bracket.games):
				viable_seeds = {game.team1_seed, game.team2_seed}
				if game.group != Game.GROUP_LOSER or game.round_number != self.round_number - 1 or self.team1_seed not in viable_seeds:
					continue
				match = game
				break
			return (match, None)

		elif self.group == Game.GROUP_WINNER:
			# Special optimization for the championship game
			if self.round_number == 0:
				if self.bracket.is_double_elimination:
					return (Game.objects.filter(bracket=self.bracket, group=Game.GROUP_WINLOSE, round_number=1)[0],
							Game.objects.filter(bracket=self.bracket, group=Game.GROUP_LOSER, round_number=0)[0])
				else:
					# Nothing happens for single elimination tournaments
					return (None, None)

			match1, match2 = None, None
			games = list(reversed(self.bracket.games))

			# Find the matching team1 seed game in the next round
			for game in games:
				viable_seeds = {game.team1_seed, game.team2_seed}
				if game.group != Game.GROUP_WINNER or game.round_number != self.round_number - 1 or self.team1_seed not in viable_seeds:
					continue
				match1 = game
				break

			if self.round_number == self.bracket.first_round:
				# Reverse iterate through all losers games until found matching team2 seed game
				for game in games:
					viable_seeds = {game.team1_seed, game.team2_seed}
					if game.group != Game.GROUP_LOSER or self.team2_seed not in viable_seeds:
						continue
					match2 = game
					break

			else:
				# Reverse iterate through losers games starting with team2 seed game = previous round's lowest seed in winners
				# Find the previous round's lowest seed
				previous_max = 0
				for game in games:
					if game.group != Game.GROUP_WINNER or game.round_number != self.round_number + 1 or game.team2_seed <= previous_max:
						continue
					previous_max = game.team2_seed

				# Get the round in the losers bracket that matches team2_seed = previous_max
				loser_round = 0
				for game in games:
					if game.group != Game.GROUP_LOSER or game.team2_seed != previous_max:
						continue
					loser_round = game.round_number
					break

				# Reverse iterate starting from loser_round
				for game in games:
					viable_seeds = {game.team1_seed, game.team2_seed}
					if game.group != Game.GROUP_LOSER or game.round_number > loser_round or self.team2_seed not in viable_seeds:
						continue
					match2 = game
					break

			return (match1, match2)
		else:
			return (None, None)

	def for_bracket(self):
		obj = {
			'id': self.pk.hex,
			'team1': Game.make_bracket_object(self.team1),
			'team2': Game.make_bracket_object(self.team2),
		}
		obj['team1']['seed'] = self.team1_seed
		obj['team1']['wins'] = self.team1_wins
		obj['team2']['seed'] = self.team2_seed
		obj['team2']['wins'] = self.team2_wins

		next_games = self.next
		obj['winner_to'] = next_games[0].id.hex if next_games[0] else None
		obj['loser_to'] = next_games[1].id.hex if next_games[1] else None

		return obj

	def save(self, *args, **kwargs):
		""" Override the save method so seeding changes propagate through the bracket

		"""
		super(Bracket, self).save(*args, **kwargs)

	def __str__(self):
		""" String representation

		"""
		try:
			return '%s - %s - %s - %s (%s:%s v %s:%s)' % (
				self.bracket.title, self.get_group_display(), self.round_number, self.number,
				self.team1.name, self.team1_wins, self.team2.name, self.team2_wins)
		except AttributeError:
			return '%s - %s - %s - %s (S%s v S%s)' % (
				self.bracket.title, self.get_group_display(), self.round_number, self.number,
				self.team1_seed, self.team2_seed)

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

class Serializer(object):
	@staticmethod
	def bracket(bracket):
		try:
			data = json.loads(bracket.as_json)
		except json.JSONDecodeError:
			data = bracket.to_dict()

		data.update({
			'id': bracket.pk.hex,
			'title': bracket.title,
			'views': 0,
			'is_finished': bracket.is_finished,
			'has_third_place': bracket.has_third_place,
			'is_double_elimination': bracket.is_double_elimination,
			'datetime': bracket.datetime,
			'date_created': bracket.date_created,
			'date_updated': bracket.date_updated,
		})

		return data
