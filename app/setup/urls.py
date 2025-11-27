from django.urls import path

from . import views

app_name = "setup"
urlpatterns = [
    path("setup/", views.setup_view, name="setup"),
    path("setup/seed/export/", views.seed_export, name="seed_export"),
    path("setup/seed/reset/", views.seed_reset, name="seed_reset"),
    path("setup/seed/clear/", views.seed_clear, name="seed_clear"),
    path("visibility/", views.visibility_list, name="visibility_list"),
    path("visibility/disabled/", views.visibility_disabled, name="visibility_disabled"),
    path("visibility/edit/", views.visibility_edit, name="visibility_edit"),
    path("visibility/delete/<int:rule_id>/", views.visibility_delete, name="visibility_delete"),
    path("visibility/picker/", views.visibility_picker, name="visibility_picker"),
]
