from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="door_index"),
    path("create/", create, name="door_create"),
    path("<slug:slug>/edit/", edit, name="door_edit"),
]
