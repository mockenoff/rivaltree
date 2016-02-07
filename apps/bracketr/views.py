"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the bracketr app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django.shortcuts import render

from apps.bracketr import models
from lib import utils

def games(request, game_id):
	""" API endpoint for games

	"""
	return utils.json_response({'game': True})

def brackets(request, bracket_id):
	""" API endpoint for brackets

	"""
	if not bracket_id:
		pass
	else:
		try:
			bracket = models.Bracket.objects.get(pk=bracket_id)
		except models.DoesNotExist:
			return utils.json_response({'error': 'No bracket with that ID'}, status_code=404)
		# return utils.json_response({'bracket': bracket.to_dict()})
		return utils.json_response({'bracket': models.Serializer.bracket(bracket)})

def test(request):
	bracket = models.Bracket.objects.get(pk='3998518876c5489bb982dbee79e4ab74')
	print(bracket.to_dict())
	# return utils.json_response({'bracket': True})
	return utils.json_response({'bracket': bracket.to_dict()})
