from django.conf.urls import url

from apps.bracketr import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]
