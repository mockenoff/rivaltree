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

	def to_dict(self):
		""" dict representation

		"""
		return {
			'id': self.id.hex,
			'email': self.user.email,
			'username': self.user.username,
			'name': ('%s %s' % (self.user.first_name, self.user.last_name)).strip(),
			'account_level': (self.account_level, self.get_account_level_display()),
		}

	def __str__(self):
		""" String representation

		"""
		return '%s (%s)' % (self.user.username, self.get_account_level_display())

	ACCOUNT_DISABLED = 1
	ACCOUNT_PENDING = 2
	ACCOUNT_BASIC = 3
	ACCOUNT_ADMIN = 4
	ACCOUNT_LEVELS = (
		(ACCOUNT_DISABLED, 'Disabled'),
		(ACCOUNT_PENDING, 'Pending'),
		(ACCOUNT_BASIC, 'Basic'),
		(ACCOUNT_ADMIN, 'Admin'),
	)

	# Tie back into the Django Users
	user = models.ForeignKey(User, db_index=True)
	account_level = models.PositiveSmallIntegerField(choices=ACCOUNT_LEVELS)

	# Object metas
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
