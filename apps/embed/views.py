"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the embed app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import uuid
import math

from django.conf import settings
from django.shortcuts import render

from apps.bracketr import models as bracketr_models

def find_matching_game(haystack, needle):
	""" Find the corresponding games for the next round

	"""
	if needle:
		for i in range(len(haystack)):
			if haystack[i]['team1']['seed'] == needle['seed'] or haystack[i]['team2']['seed'] == needle['seed']:
				return haystack[i]
	return None

def normalize_bracket(games):
	""" Normalize a list of games for Django display

	"""
	game_total = 0
	next_round = None
	new_games = None

	for i in range(len(games)):
		if i > 0:
			new_games = []
			next_round = games[i - 1]
			game_total = int(math.pow(2, i - 1))

			for j in range(game_total):
				if next_round:
					new_games.append(find_matching_game(games[i], next_round[j]['team1'] if next_round[j] else None))
					new_games.append(find_matching_game(games[i], next_round[j]['team2'] if next_round[j] else None))
				else:
					new_games.extend([None, None])

			games[i] = new_games

	games.reverse()
	return games

def index(request, bracket_id=None):
	""" Serve up an embeddable widget

	"""
	try:
		bracket = bracketr_models.Bracket.objects.get(pk=bracket_id)
	except (bracketr_models.Bracket.DoesNotExist, ValueError):
		return render(request, 'embed/embed.html', {
			'bracket': None,
			'uuid': uuid.uuid4().hex,
			'ws_url': '%s:%s%s' % (settings.WS_URL, settings.WS_PORT, settings.WS_BASE),
		}, status=404)

	bracket = bracketr_models.Serializer.bracket(bracket)
	for key in ['winners', 'losers']:
		if key in bracket:
			bracket[key] = normalize_bracket(bracket[key])

	# Buffer out winners and losers to keep columns even
	if bracket['is_double_elimination']:
		winners_total = len(bracket['winners'])
		losers_total = len(bracket['losers'])
		if winners_total < losers_total:
			bracket['winners'] = [[] for i in range(losers_total - winners_total)] + bracket['winners']
		elif losers_total < winners_total:
			bracket['losers'] = [[] for i in range(winners_total - losers_total)] + bracket['losers']

	return render(request, 'embed/embed.html', {
		'bracket': bracket,
		'uuid': uuid.uuid4().hex,
		'ws_url': '%s:%s%s' % (settings.WS_URL, settings.WS_PORT, settings.WS_BASE),
	})

def console(request):
	return render(request, 'embed/console.html', {
		'ws_url': '%s:%s%s' % (settings.WS_URL, settings.WS_PORT, settings.WS_BASE),
	})

def sandbox(request):
	return render(request, 'embed/sandbox.html')
