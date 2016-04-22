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
	if bracket_type not in ('single', 'double'):
		is_valid = 'Invalid bracketType'
	elif use_participants and (not isinstance(list_items, list) or not list_items):
		is_valid = 'Need some participants since useParticipants is true'
	elif not use_participants and (not isinstance(num_participants, int) or num_participants < 1):
		is_valid = 'Invalid numParticipants'

	if is_valid != True:
		return utils.json_response({'error': is_valid}, status_code=400)

	return utils.json_response({'bracket': None})
