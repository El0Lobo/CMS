from django.urls import path
from .views import index, create, edit
urlpatterns = [
    path('', index, name='pages_index'),
    path('create/', create, name='pages_create'),
    path('<slug:slug>/edit/', edit, name='pages_edit'),
]
