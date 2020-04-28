from django.urls import path
from links.views import link_list,tagged


urlpatterns = [
	path('',link_list, name='link_list'),
	path('tag/<slug:slug>/',tagged,name="tagged"),
]