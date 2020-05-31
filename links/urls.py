from django.urls import path
from links.views import link_list, tagged, link_remove


urlpatterns = [
    path("", link_list, name="link_list"),
    path("tag/<slug:slug>/", tagged, name="tagged"),
    path("link/<pk>/remove/", link_remove, name="link_remove"),
]
