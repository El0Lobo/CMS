from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="maps_index"),
    path("create/", create, name="maps_create"),
    path("<slug:slug>/edit/", edit, name="maps_edit"),
]
