from django.urls import path
from . import views

app_name = "setup"
urlpatterns = [
    path("setup/", views.setup_view, name="setup"),
    path("visibility/", views.visibility_list, name="visibility_list"),
    path("visibility/edit/", views.visibility_edit, name="visibility_edit"),
    path("visibility/delete/<int:rule_id>/", views.visibility_delete, name="visibility_delete"),
    path("visibility/picker/", views.visibility_picker, name="visibility_picker"),
]
