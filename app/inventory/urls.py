from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="inventory_index"),
    path("create/", create, name="inventory_create"),
    path("<slug:slug>/edit/", edit, name="inventory_edit"),
]
