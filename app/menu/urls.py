from django.urls import path
from . import views

app_name = "menu"

urlpatterns = [
    path("", views.manage_menu, name="manage"),  # resolves to /cms/menu/
    path("items/", views.items_list, name="items_list"),
    path("categories/new/<slug:root>/", views.category_create, name="category_create_root"),
    path("categories/new/sub/<slug:parent_slug>/", views.category_create, name="category_create_sub"),
    path("categories/<slug:slug>/edit/", views.category_edit, name="category_edit"),
    path("categories/<slug:slug>/delete/", views.category_delete, name="category_delete"),
    path("items/new/<slug:parent_slug>/", views.item_create, name="item_create_here"),
    path("items/<slug:slug>/edit/", views.item_edit, name="item_edit"),
    path("item/<slug:slug>/delete/", views.item_delete, name="item_delete"),
]
