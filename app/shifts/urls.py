from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="shifts_index"),
    path("create/", create, name="shifts_create"),
    path("<slug:slug>/edit/", edit, name="shifts_edit"),
]
