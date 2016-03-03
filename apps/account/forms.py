"""
.. module:: forms
	:platform: Unix
	:synopsis: Contains the forms

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django import forms

class ContactForm(forms.Form):
	name = forms.CharField(label='Your name')
	email = forms.EmailField(label='Your email')
	message = forms.CharField(label='Your message', widget=forms.Textarea(attrs={'rows': 3}))

	def __init__(self, *args, **kwargs):
		""" Override __init__ to add error class to fields

		"""
		super(ContactForm, self).__init__(*args, **kwargs)
		for field in ('name', 'email', 'message'):
			if field in self.errors and self.errors[field]:
				print(field, self.errors[field])
				try:
					classes = self.fields[field].widget.attrs['class'].split(' ')
				except KeyError:
					classes = []
				classes.append('error')
				self.fields[field].widget.attrs['class'] = ' '.join(classes)
