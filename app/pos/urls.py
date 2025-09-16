from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="pos_index"),
    path("create/", create, name="pos_create"),
    path("<slug:slug>/edit/", edit, name="pos_edit"),
]
