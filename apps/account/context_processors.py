"""
.. module:: context_processors
   :platform: Unix
   :synopsis: Contains the context processors for all of the apps

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from apps.account import models

def manager_processor(request):
	""" Return the associated manager object if a user is logged in

	"""
	if not request.path.startswith('/api/') and not request.path.startswith('/admin/') and request.user and request.user.is_authenticated():
		manager = models.Manager.objects.filter(user=request.user)
		if manager:
			manager = manager[0]
			return {'manager': {
				'id': manager.id.hex,
				'email': request.user.email,
				'username': request.user.username,
				'name': ' '.join([request.user.first_name, request.user.last_name]).strip(),
				'account_level': (manager.account_level, manager.get_account_level_display()),
			}}
	return {'manager': None}

def global_vars(request):
	""" Return a set of global variables

	"""
	return {
		'DEFAULT_TITLE': 'Plant those rival seeds',
		'DEFAULT_DESCRIPTION': 'Generate brackets and manage real-time updating tournaments',
	}
