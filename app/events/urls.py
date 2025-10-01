from django.urls import path

from app.events import views

app_name = "events"


urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create, name="create"),
    path("<slug:slug>/edit/", views.edit, name="edit"),
    path("<slug:slug>/delete/", views.delete, name="delete"),
    path("<slug:slug>/", views.detail, name="detail"),
]
