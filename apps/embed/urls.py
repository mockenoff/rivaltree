from django.conf.urls import url
from django.conf import settings

from apps.embed import views

urlpatterns = [
	url(r'^(?P<bracket_id>[^/]+)?', views.index, name='index'),
]

if settings.DEBUG:
	urlpatterns.insert(0, url(r'^console', views.console, name='console'))
	urlpatterns.insert(0, url(r'^sandbox', views.sandbox, name='sandbox'))
