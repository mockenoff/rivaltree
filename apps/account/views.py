"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the account app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import random

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from lib import utils
from apps.account import models

def index(request):
	""" Serve up the index page

	"""
	heroes = ('bowling', 'futbol', 'grass', 'haze', 'soccer', 'sundown', 'tennis', 'dota', 'cod',)
	return render(request, 'main.html', {'hero': random.choice(heroes)})

def about(request):
	""" Serve up the about page

	"""
	return render(request, 'about.html')

def contact(request):
	""" Serve up the contact page

	"""
	return render(request, 'contact.html')

@csrf_exempt
def users(request, action=None):
	""" Serve up the users API endpoint

	"""
	if request.user and request.user.is_authenticated():
		if action == 'logout' and request.method == 'POST':
			logout(request)
			return utils.json_response({'logged_in': False})

		try:
			return utils.json_response({'user': models.Manager.objects.filter(user=request.user)[0].to_dict()})
		except IndexError:
			return utils.json_response({'logged_in': True, 'error': 'No associated manager'}, status_code=500)

	else:
		if action == 'login' and request.method == 'POST':
			user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
			if user:
				login(request, user)
				request.user = user
				return users(request)

		return utils.json_response({'logged_in': False}, status_code=401)

def dash(request):
	""" Serve up the dash page (catchall view for dash requests)

	"""
	return render(request, 'index.html')
