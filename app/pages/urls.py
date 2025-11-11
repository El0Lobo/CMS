from django.urls import path

from . import api_views
from .views import create, edit, index, preview

urlpatterns = [
    path("", index, name="pages_index"),
    path("create/", create, name="pages_create"),
    path("preview/", preview, name="pages_preview"),
    path("api/events/", api_views.events_feed, name="pages_api_events"),
    path("api/menu/", api_views.menu_snapshot, name="pages_api_menu"),
    path("api/site/", api_views.site_context, name="pages_api_site"),
    path("api/assets/", api_views.assets_library, name="pages_api_assets"),
    path("api/pages/", api_views.page_create, name="pages_api_create"),
    path("api/pages/<slug:slug>/", api_views.page_detail, name="pages_api_detail"),
    path("api/preview/html/", api_views.preview_html, name="pages_api_preview_html"),
    path("<slug:slug>/edit/", edit, name="pages_edit"),
]
