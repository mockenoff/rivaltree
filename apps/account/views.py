"""
.. module:: views
   :platform: Unix
   :synopsis: Contains the views for the account app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import random
import datetime

from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
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
			did_send = utils.send_template_mail(
				subject='Rivaltree Contact Form - %s' % datetime.datetime.now().strftime('%B %d, %Y at %I:%M:%S %p'),
				from_email=form.cleaned_data['email'],
				recipient_list=[settings.DEFAULT_CONTACT_EMAIL],
				template='contact',
				data=form.cleaned_data,
			)
			form = forms.ContactForm()
	else:
		form = forms.ContactForm()

	return render(request, 'contact.html', {'form': form, 'did_send': did_send})

def signup(request):
	""" Serve up the signup page

	"""
	if request.user.is_authenticated():
		return redirect('/')

	form = None
	if request.method == 'POST':
		form = forms.SignupForm(request.POST)
		if form.is_valid():
			user, manager, confirmation = models.create_manager(
				username=form.cleaned_data['username'].lower(),
				email=form.cleaned_data['email'].lower(),
				password=form.cleaned_data['password'])

			utils.send_template_mail(
				subject='Confirm your Rivaltree account',
				from_email=settings.DEFAULT_CONTACT_EMAIL,
				recipient_list=[user.email],
				template='confirm',
				data={
					'username': user.username,
					'email': user.email,
					'token': confirmation.id.hex,
				})

			user = authenticate(username=user.username, password=form.cleaned_data['password'])
			login(request, user)
			return redirect('/dash/')
	else:
		form = forms.SignupForm()
	return render(request, 'signup.html', {'form': form})

def confirm(request, token=None):
	""" Do account confirmations

	"""
	try:
		confirmation = models.Confirmation.objects.get(pk=token)
	except (ValueError, models.Confirmation.DoesNotExist):
		confirmation = False

	if confirmation:
		confirmation.confirm()
		confirmation.manager.user.backend = 'django.contrib.auth.backends.ModelBackend'
		login(request, confirmation.manager.user)
		return redirect('/dash/')
	elif not token:
		return redirect('/')
	else:
		return render(request, 'confirm_fail.html', {'token': token}, status=400)

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

def forgot(request, token=None):
	""" Reset the password

	"""
	if request.user.is_authenticated():
		return redirect('/')

	form = None
	error = False
	complete = False

	if token:
		try:
			reset = models.Reset.objects.get(pk=token)
		except (ValueError, models.Reset.DoesNotExist):
			reset = False
			error = 1

		form = forms.ResetForm()

		if reset:
			if request.method == 'POST':
				form = forms.ResetForm(request.POST)
				if form.is_valid():
					reset.reset(password=form.cleaned_data['password'])
					complete = True
				else:
					error = 2
	else:
		if request.method == 'POST':
			form = forms.ForgotForm(request.POST)
			if form.is_valid():
				manager = models.Manager.objects.filter(user__email=form.cleaned_data['email'].lower()).first()
				if manager:
					reset = models.Reset.objects.filter(manager=manager).first()
					if not reset:
						reset = models.Reset.objects.create(manager=manager)

					utils.send_template_mail(
						subject='Reset the password to your Rivaltree account',
						from_email=settings.DEFAULT_CONTACT_EMAIL,
						recipient_list=[manager.user.email],
						template='forgot',
						data={
							'username': manager.user.username,
							'email': manager.user.email,
							'token': reset.id.hex,
						})
					complete = True
				else:
					error = True
		else:
			form = forms.ForgotForm()

	return render(request, 'forgot.html', {
		'form': form,
		'token': token,
		'error': error,
		'complete': complete,
	})

def login_view(request):
	""" Log in the user

	"""
	if request.user.is_authenticated():
		return redirect('/')

	form = None
	error = False
	if request.method == 'POST':
		form = forms.LoginForm(request.POST)
		if form.is_valid():
			user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password'])
			if user:
				login(request, user)
				return redirect(request.GET.get('next', '/'))
			else:
				error = True
	else:
		form = forms.LoginForm()

	return render(request, 'login.html', {'form': form, 'error': error})

def logout_view(request):
	""" Log out the user

	"""
	if request.user.is_authenticated():
		logout(request)
	return redirect('/')

def emails(request, template):
	""" Debug view for email templates

	"""
	data = {}
	if template == 'contact':
		data.update({
			'name': 'Test Name',
			'email': 'test@email.com',
			'message': 'This is a test message.\n\nHere\'s a new line.',
		})
	elif template == 'confirm':
		data.update({
			'username': 'testuser',
			'email': 'test@email.com',
			'token': '7f94097c3ca8415ab209fe6c1c063b07',
		})
	elif template == 'forgot':
		data.update({
			'username': 'testuser',
			'email': 'test@email.com',
			'token': '7f94097c3ca8415ab209fe6c1c063b07',
		})
	return render(request, 'emails/%s.html' % template, data)

@login_required(login_url='/login/')
def dash(request):
	""" Serve up the dash page (catchall view for dash requests)

	"""
	return render(request, 'index.html')
