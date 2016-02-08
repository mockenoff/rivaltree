"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the bracketr app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.bracketr import models
from lib import utils

@csrf_exempt
def games(request, game_id):
	""" API endpoint for games

	"""
	return utils.json_response({'game': True})

@csrf_exempt
def brackets(request, bracket_id):
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

def test(request):
	bracket = models.Bracket.objects.get(pk='3998518876c5489bb982dbee79e4ab74')
	print(bracket.to_dict())
	return utils.json_response({'bracket': True})
	return utils.json_response({'bracket': bracket.to_dict()})
