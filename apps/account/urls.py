from django.conf.urls import url

from apps.account import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^api/users/(?P<user_id>[^/]+)?', views.users, name='users'),
	url(r'^dash/', views.dash, name='dash'),
]
