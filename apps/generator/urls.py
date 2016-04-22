from django.conf.urls import url
from django.conf import settings

from apps.generator import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
]
