"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the bracketr app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import simplejson as json

from django.shortcuts import render
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt

from apps.bracketr import models
from lib import utils

@csrf_exempt
def games(request, game_id=None):
	""" API endpoint for games

	"""
	return utils.json_response({'game': True})

@csrf_exempt
def teams(request, team_id=None):
	""" API endpoint for teams

	"""
	if not request.user.is_authenticated():
		return utils.json_response({'logged_in': False}, status_code=401)

	if team_id:
		try:
			team = models.Team.objects.get(pk=team_id)
		except models.Team.DoesNotExist:
			return utils.json_response({'error': 'No team with that ID'}, status_code=404)

		if request.method == 'PUT':
			form_data = json.loads(request.readline())
			team.name = form_data['team']['name']
			team.header_path = form_data['team']['header_path'] # ENHANCEMENT: Only for premium users?
			team.starting_seed = form_data['team']['starting_seed']

			try:
				team.save()
			except ValidationError: # BUG: header_path validation
				return utils.json_response({'error': 'Could not save team'}, status_code=400)

		return utils.json_response({'team': models.Serializer.team(team)})

	else:
		bracket_id = request.GET.get('bracket_id')
		if bracket_id:
			try:
				bracket = models.Bracket.objects.get(pk=bracket_id)
			except models.Bracket.DoesNotExist:
				return utils.json_response({'error': 'No bracket with that ID'}, status_code=404)

			teams = models.Team.objects.filter(bracket=bracket_id).order_by('starting_seed', 'date_updated')
			return utils.json_response({'teams': [models.Serializer.team(team) for team in teams]})

		else:
			return utils.json_response({'error': 'Can\'t return all teams'}, status_code=500)

@csrf_exempt
def brackets(request, bracket_id=None):
	""" API endpoint for brackets

	"""
	if not request.user.is_authenticated():
		return utils.json_response({'logged_in': False}, status_code=401)

	elif not bracket_id:
		return utils.json_response({
			'brackets': [
				models.Serializer.bracket(bracket) for bracket in
				models.Bracket.objects.filter(manager__user=request.user).order_by('date_updated')
			],
		})

	else:
		try:
			bracket = models.Bracket.objects.get(pk=bracket_id)
		except models.Bracket.DoesNotExist:
			return utils.json_response({'error': 'No bracket with that ID'}, status_code=404)
		# return utils.json_response({'bracket': bracket.to_dict()})
		return utils.json_response({'bracket': models.Serializer.bracket(bracket)})

def crown(request):
	""" Randomize color of SVG crown

	"""
	import random

	choices = []
	colors = ['#2696A5', '#42464E', '#FFA000', '#5BA500']

	for i in range(3):
		choice = random.choice(colors)
		colors.remove(choice)
		choices.append(choice)

	return render(request, 'crown.svg', {'colors': choices}, content_type='image/svg+xml')

def test(request):
	bracket = models.Bracket.objects.get(pk='3998518876c5489bb982dbee79e4ab74')
	print(bracket.to_dict())
	return utils.json_response({'bracket': True})
	return utils.json_response({'bracket': bracket.to_dict()})
