"""
.. module:: filters
   :platform: Unix
   :synopsis: Contains the filters for the embed app

.. moduleauthor:: Tim <timothycpoon@gmail.com>

"""

from django import template

register = template.Library()

@register.filter(name='lookup')
def lookup(value, key):
	return value[key]
