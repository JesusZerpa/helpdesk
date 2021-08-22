from django.urls import path
from .views import *
urlpatterns=[
	path("",index),
	path("faq/",faq),
	path("faq/<name>/",faq),
	path("login/",login),
	]
Tickets("<service>/tikects/",urlpatterns)