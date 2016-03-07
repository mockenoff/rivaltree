"""
.. module:: forms
	:platform: Unix
	:synopsis: Contains the forms

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django import forms

class ErrorForm(forms.Form):
	ERROR_FIELDS = []

	def __init__(self, *args, **kwargs):
		""" Override __init__ to add error class to fields

		"""
		super(ErrorForm, self).__init__(*args, **kwargs)
		for field in self.ERROR_FIELDS:
			if field in self.errors and self.errors[field]:
				try:
					classes = self.fields[field].widget.attrs['class'].split(' ')
				except KeyError:
					classes = []
				classes.append('error')
				self.fields[field].widget.attrs['class'] = ' '.join(classes)

class ResetForm(ErrorForm):
	password = forms.CharField(label='Your new password', widget=forms.PasswordInput, min_length=6, help_text='At least 6 characters long')
	ERROR_FIELDS = ('password')

class ForgotForm(ErrorForm):
	email = forms.EmailField(label='Your email')
	ERROR_FIELDS = ('email')

class LoginForm(ErrorForm):
	username = forms.CharField(label='Your username')
	password = forms.CharField(label='Your password', widget=forms.PasswordInput)
	ERROR_FIELDS = ('username', 'password')

class SignupForm(ErrorForm):
	username = forms.CharField(label='Your username')
	email = forms.EmailField(label='Your email')
	password = forms.CharField(label='Your password', widget=forms.PasswordInput, min_length=6, help_text='At least 6 characters long')
	ERROR_FIELDS = ('username', 'email', 'password')

class ContactForm(ErrorForm):
	name = forms.CharField(label='Your name')
	email = forms.EmailField(label='Your email')
	message = forms.CharField(label='Your message', widget=forms.Textarea(attrs={'rows': 3}))
	ERROR_FIELDS = ('name', 'email', 'message')
