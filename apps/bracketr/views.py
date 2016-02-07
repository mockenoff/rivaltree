"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the bracketr app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django.shortcuts import render
from django.http import JsonResponse

from apps.bracketr import models

def index(request):
	""" Serve up the index page

	"""
	bracket = models.Bracket.objects.get(pk='3998518876c5489bb982dbee79e4ab74')
	print(bracket.to_dict())
	# return _json_response({'bracket': True})
	return _json_response({'bracket': bracket.to_dict()})

def _json_response(data, status_code=200):
	response = JsonResponse(data, status=status_code)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
	response['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With'
	return response
