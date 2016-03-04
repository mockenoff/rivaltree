"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the account app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import random
import datetime
from xml.etree import ElementTree

from django.conf import settings
from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout

from lib import utils
from apps.account import forms
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
	form = None
	did_send = False

	if request.method == 'POST':
		form = forms.ContactForm(request.POST)
		if form.is_valid():
			template_string = get_template('emails/contact.html').render({
				'name': form.cleaned_data['name'],
				'email': form.cleaned_data['email'],
				'message': form.cleaned_data['message'],
			})
			message_string = ''.join(ElementTree.fromstring(template_string).itertext())
			send_mail(
				subject='Rivaltree Contact Form - %s' % datetime.datetime.now().strftime('%B %d, %Y at %I:%M:%S %p'),
				message=message_string,
				html_message=template_string,
				from_email=form.cleaned_data['email'],
				recipient_list=[settings.DEFAULT_CONTACT_EMAIL],
				fail_silently=False
			)
			did_send = True
			form = forms.ContactForm()
	else:
		form = forms.ContactForm()

	return render(request, 'contact.html', {'form': form, 'did_send': did_send})

def terms(request):
	""" Serve up the terms page

	"""
	return render(request, 'terms.html')

def privacy(request):
	""" Serve up the privacy page

	"""
	return render(request, 'privacy.html')

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
