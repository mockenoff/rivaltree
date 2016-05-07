"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the generator app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import simplejson as json

from django.shortcuts import render

from lib import utils
from apps.bracketr import models

def index(request):
	""" Front end interface for the generator

	"""
	if request.GET.get('format') == 'json':
		try:
			num_participants = int(request.GET.get('numParticipants'))
		except (TypeError, ValueError):
			num_participants = None
		return generateBracket(
			bracket_type=request.GET.get('bracketType'),
			has_round_robin=True if request.GET.get('hasRoundRobin') == 'true' else False,
			use_participants=True if request.GET.get('useParticipants') == 'true' else False,
			num_participants=num_participants,
			list_items=request.GET.getlist('listItems', None))

	return render(request, 'generator/index.html')

def generateBracket(bracket_type, has_round_robin, use_participants, num_participants=None, list_items=None):
	""" Generate a JSON bracket

	"""
	is_valid = True
	if bracket_type not in ('single', 'double', 'round-robin'):
		is_valid = 'Invalid bracketType'
	elif use_participants and (not isinstance(list_items, list) or not list_items):
		is_valid = 'Need some participants since useParticipants is true'
	elif not use_participants and (not isinstance(num_participants, int) or num_participants < 1):
		is_valid = 'Invalid numParticipants'

	if is_valid != True:
		return utils.json_response({'error': is_valid}, status_code=400)

	if not use_participants:
		list_items = [str(index + 1) for index in range(num_participants)]

	bracket = models.Bracket(
		has_round_robin=has_round_robin,
		is_double_elimination=True if bracket_type == 'double' else False)

	teams = [models.Team(
		name=list_items[index],
		starting_seed=index + 1,
		bracket=bracket) for index in range(len(list_items))]

	data = {
		'teams': {team.id.hex: {
			'name': team.name,
			'seed': team.starting_seed,
		} for team in teams},
		'seeds': {team.starting_seed: team.id.hex for team in teams},
	}

	if has_round_robin or bracket_type == 'round-robin':
		data['round_robin'] = bracket.make_round_robin(teams=teams, save=False)[0]

	if bracket_type != 'round-robin':
		data['winners'] = bracket.make_bracket(teams=teams, group=models.Game.GROUP_WINNER, fill=True, save=False)[0]

	if bracket_type == 'double':
		data['losers'], games = bracket.make_losers_bracket(data['winners'], save=False)
		data['winner_loser'], games = bracket.make_winlose_bracket(save=False)

	print('ASDF', data)

	return utils.json_response({'bracket': data})
