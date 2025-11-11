from __future__ import annotations

from django.utils.text import slugify

from .models import SiteSettings
from app.pages.navigation import ensure_pages_from_settings, get_navigation_entries


def site_settings_context(request):
    settings_obj = SiteSettings.get_solo()

    # Ensure legacy required_pages entries exist as Page records
    ensure_pages_from_settings(settings_obj)

    nav_entries = get_navigation_entries()
    pages = [
        {
            "title": entry.title,
            "slug": entry.slug,
            "url": entry.url,
            "pretty_slug": entry.pretty_slug,
            "pretty_url": entry.pretty_url,
        }
        for entry in nav_entries
    ]

    # Determine active nav item
    req_slug = None
    if getattr(request, "resolver_match", None):
        req_slug = request.resolver_match.kwargs.get("slug")
    if req_slug is None and request.path == "/":
        req_slug = "home"

    current_nav_title = None
    if req_slug:
        lookup = slugify(req_slug) or req_slug
        for entry in nav_entries:
            if entry.slug == lookup or entry.pretty_slug == lookup:
                current_nav_title = entry.title
                break

    # Address helpers
    street = (settings_obj.address_street or "").strip()
    number = (settings_obj.address_number or "").strip()
    postal = (settings_obj.address_postal_code or "").strip()
    city = (settings_obj.address_city or "").strip()
    country = (settings_obj.address_country or "").strip()

    line1 = " ".join(x for x in [street, number] if x) if street else ""
    line2 = " ".join(x for x in [postal, city] if x)
    line3 = country
    has_any = any([line1, line2, line3])
    compact = ", ".join(x for x in [line1, line2, line3] if x)

    return {
        "site_settings": settings_obj,
        "public_pages": pages,
        "current_nav_title": current_nav_title,
        "site_address_has_any": has_any,
        "site_address_line1": line1,
        "site_address_line2": line2,
        "site_address_line3": line3,
        "site_address_compact": compact,
    }
