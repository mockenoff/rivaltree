"""
.. module:: utils
   :platform: Unix
   :synopsis: Various utility methods

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

import simplejson as json

from django.http import JsonResponse

def get_form_data(request):
	""" Return the embedded form data of an HTTP request

	:param request: Django request object
	:type request: Django request object
	:returns: dict

	"""
	return json.loads(request.readline())

def update_model(model, data, keys=None):
	""" Update a model's attributes with a bunch of data

	:param model: The model to update
	:type model: Django model
	:param data: Data values to copy over to the model
	:type data: dict
	:param keys: Specify which keys to update (if None, will update all in data)
	:type keys: list

	"""
	if keys:
		for key in keys:
			if key in data:
				model.__setattr__(key, data[key])
	else:
		for key, val in data.items():
			model.__setattr__(key, val)
	return model

def json_response(data, status_code=200):
	""" Take a data dict and turn it into a JSON response

	:param data: Dict of response data
	:type data: dict
	:param status_code: HTTP status code to return with
	:type status_code: int

	"""
	response = JsonResponse(data, status=status_code)
	response['Access-Control-Allow-Origin'] = '*'
	response['Access-Control-Allow-Methods'] = 'GET, PUT, POST, DELETE, OPTIONS'
	response['Access-Control-Allow-Headers'] = 'Content-Type, Access-Control-Allow-Headers, Authorization, X-Requested-With'
	return response
