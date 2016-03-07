from django.conf.urls import url
from django.conf import settings

from apps.account import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^about/$', views.about, name='about'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'^confirm/(?P<token>[^/]+)?', views.confirm, name='confirm'),
	url(r'^contact/$', views.contact, name='contact'),
	url(r'^terms/$', views.terms, name='terms'),
	url(r'^privacy/$', views.privacy, name='privacy'),
	url(r'^api/users/(?P<action>[^/]+)?', views.users, name='users'),
	url(r'^logout/$', views.logout_view, name='logout'),
	url(r'^login/$', views.login_view, name='login'),
	url(r'^forgot/(?P<token>[^/]+)?', views.forgot, name='forgot'),
	url(r'^dash/', views.dash, name='dash'),
]

if settings.DEBUG:
	urlpatterns.append(url(r'^emails/(?P<template>[^/]+)', views.emails, name='emails'))
