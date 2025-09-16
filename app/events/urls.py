from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="events_index"),
    path("create/", create, name="events_create"),
    path("<slug:slug>/edit/", edit, name="events_edit"),
]
