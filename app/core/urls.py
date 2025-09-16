from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from .views import health

urlpatterns = [
    # Admin & health
    path("admin/", admin.site.urls),
    path("health/", health, name="health"),

    # Auth
    path("accounts/", include("django.contrib.auth.urls")),

    # -------- Public --------
    # Main public site (pages)
    path("", include(("app.pages.urls_public", "public"), namespace="public")),
    # Public merch (e.g. /shop/…)
    path("", include(("app.merch.urls_public", "merch_public"), namespace="merch_public")),
    # Public menu (e.g. /menu/…)
    path("menu/", include(("app.public.menu.urls", "public_menu"), namespace="public_menu")),

    # -------- CMS --------
    path("cms/", include("app.cms.urls")),
    path("cms/pages/", include("app.pages.urls")),
    path("cms/blog/", include("app.blog.urls")),
    path("cms/events/", include("app.events.urls")),
    path("cms/shifts/", include("app.shifts.urls")),
    path("cms/door/", include("app.door.urls")),
    path("cms/merch/", include(("app.merch.urls", "merch"), namespace="merch")),
    path("cms/inventory/", include("app.inventory.urls")),
    path("cms/accounting/", include("app.accounting.urls")),
    path("cms/social/", include("app.social.urls")),
    path("cms/automation/", include("app.automation.urls")),
    path("cms/maps/", include("app.maps.urls")),
    path("cms/settings/", include("app.setup.urls")),
    path("cms/users/", include("app.users.urls")),
    path("", include("app.bands.urls", namespace="bands")),          
    path("", include("app.bands.public_urls", namespace="bands_pub")),
    path("cms/menu/", include(("app.menu.urls", "menu"), namespace="menu")),
    path("cms/assets/", include("app.assets.urls")),   
    path("cms/inbox/", include(("app.comms.urls", "comms"), namespace="comms")),
]

# Media during development
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
