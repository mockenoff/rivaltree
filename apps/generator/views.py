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
	return render(request, 'generator/index.html')

def json(request):
	""" Backend API for the generator

	"""
	return utils.json_response({'bracket': None})
