from django.conf.urls import url

from apps.embed import views

urlpatterns = [
	url(r'^(?P<bracket_id>[^/]+)?', views.index, name='index'),
]
