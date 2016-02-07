"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the account app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django.shortcuts import render

from lib import utils
from apps.account import models

def index(request):
	""" Serve up the index page

	"""
	return render(request, 'main.html')

def users(request, user_id):
	""" Serve up the users API endpoint

	"""
	if request.user.is_authenticated():
		try:
			return utils.json_response({'user': models.Manager.objects.filter(user=request.user)[0].to_dict()})
		except IndexError:
			return utils.json_response({'logged_in': True, 'error': 'No associated manager'}, status_code=500)
	else:
		return utils.json_response({'logged_in': False}, status_code=401)

def dash(request):
	""" Serve up the dash page (catchall view for dash requests)

	"""
	return render(request, 'index.html')
