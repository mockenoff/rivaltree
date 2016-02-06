"""
.. module:: models
   :platform: Unix
   :synopsis: Contains the models for the account app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import uuid

from django.db import models
from django.contrib.auth.models import User

class Manager(models.Model):
	""" Manager model

	"""

	def __str__(self):
		""" String representation

		"""
		return '%s (%s)' % (self.user.username, self.get_account_level_display())

	ACCOUNT_ACTIVE = 1
	ACCOUNT_DISABLED = 2
	ACCOUNT_LEVELS = (
		(ACCOUNT_ACTIVE, 'Active'),
		(ACCOUNT_DISABLED, 'Disabled'),
	)

	# Tie back into the Django Users
	user = models.ForeignKey(User, db_index=True)
	account_level = models.PositiveSmallIntegerField(choices=ACCOUNT_LEVELS)

	# Object metas
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
