"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the embed app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django.shortcuts import render, redirect

from apps.bracketr import models as bracketr_models

def index(request, bracket_id=None):
	""" Serve up an embeddable widget

	"""
	try:
		bracket = bracketr_models.Bracket.objects.get(pk=bracket_id)
	except (bracketr_models.Bracket.DoesNotExist, ValueError):
		bracket = None
	return render(request, 'embed.html', {
		'bracket': bracketr_models.Serializer.bracket(bracket),
	})
