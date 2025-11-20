from django.urls import path

from .views import create, edit, index

urlpatterns = [
    path("", index, name="inventory_index"),
    path("create/", create, name="inventory_create"),
    path("<slug:slug>/edit/", edit, name="inventory_edit"),
]
