from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="social_index"),
    path("create/", create, name="social_create"),
    path("<slug:slug>/edit/", edit, name="social_edit"),
]
