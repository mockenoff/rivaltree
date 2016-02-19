from django.conf.urls import url

from apps.account import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^api/users/(?P<action>[^/]+)?', views.users, name='users'),
	url(r'^dash/', views.dash, name='dash'),
]
