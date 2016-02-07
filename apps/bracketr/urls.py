from django.conf.urls import url

from apps.bracketr import views

urlpatterns = [
	url(r'^games/(?P<game_id>[^/]+)?', views.games, name='games'),
	url(r'^brackets/(?P<bracket_id>[^/]+)?', views.brackets, name='brackets'),
	url(r'^test/$', views.test, name='test'),
]
