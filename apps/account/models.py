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
	user = models.OneToOneField(User, on_delete=models.CASCADE, db_index=True)
	account_level = models.PositiveSmallIntegerField(choices=ACCOUNT_LEVELS, default=ACCOUNT_PENDING)

	# Object metas
	date_created = models.DateTimeField(auto_now_add=True)
	date_updated = models.DateTimeField(auto_now=True)
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)


class Confirmation(models.Model):
	""" Confirmation Model

	"""

	def confirm(self):
		""" Confirm out a pending confirmation

		"""
		if self.manager.account_level == 2:
			self.manager.account_level = 3
			self.manager.save()
		self.delete()

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	manager = models.ForeignKey(Manager, db_index=True)
	date_created = models.DateTimeField(auto_now_add=True)


class Reset(models.Model):
	""" Reset model

	"""

	def reset(self, password):
		""" Reset a user password

		:param password: New user password
		:type password: str

		"""
		self.manager.user.set_password(password)
		self.manager.user.save()
		self.delete()

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	manager = models.ForeignKey(Manager, db_index=True)
	date_created = models.DateTimeField(auto_now_add=True)


def create_manager(username, email, password):
	""" All the steps to creating a fresh Manager object

	"""
	user = User.objects.create_user(username=username, email=email, password=password)
	manager = Manager.objects.create(user=user)
	confirmation = Confirmation.objects.create(manager=manager)
	return user, manager, confirmation
