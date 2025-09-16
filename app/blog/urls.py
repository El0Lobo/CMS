from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path("", index, name="blog_index"),
    path("create/", create, name="blog_create"),
    path("<slug:slug>/edit/", edit, name="blog_edit"),
]
