from django.urls import reverse, NoReverseMatch
from django.utils.text import slugify
from .models import SiteSettings

def _parse_page_line(line: str):
    raw = (line or "").strip()
    if not raw:
        return None
    if "|" in raw:
        slug_part, label_part = raw.split("|", 1)
        slug  = (slug_part or "").strip()
        title = (label_part or "").strip()
        if not slug:
            slug = slugify(title) or "page"
        if not title:
            title = slug
    else:
        title = raw
        slug  = slugify(title) or "page"
    return slug, title

def _reverse_canonical(slug: str) -> str:
    for name in ("pages:detail", "pages:page", "page-detail"):
        try:
            return reverse(name, kwargs={"slug": slug})
        except NoReverseMatch:
            continue
    return "/" if slug == "home" else f"/{slug}/"

def site_settings_context(request):
    settings_obj = SiteSettings.get_solo()

    raw_lines = [
        ln.strip()
        for ln in (settings_obj.required_pages or "").splitlines()
        if ln.strip()
    ]

    pages = []
    seen_slugs = set()

    for line in raw_lines:
        parsed = _parse_page_line(line)
        if not parsed:
            continue
        slug, title = parsed
        if slug in seen_slugs:
            continue
        seen_slugs.add(slug)

        # canonical (by slug)
        url = _reverse_canonical(slug)

        # pretty (by label)
        pretty_slug = slugify(title) or slug
        pretty_url  = "/" if pretty_slug == "home" else f"/{pretty_slug}/"

        pages.append({
            "title": title,           # label to show in nav & tab
            "slug": slug,             # canonical slug (DB)
            "url": url,               # canonical URL
            "pretty_slug": pretty_slug,
            "pretty_url": pretty_url, # URL we’ll show in the nav
        })

    # Which label should the current page show?
    req_slug = None
    if getattr(request, "resolver_match", None):
        req_slug = request.resolver_match.kwargs.get("slug")
    if req_slug is None and request.path == "/":
        req_slug = "home"

    current_nav_title = None
    if req_slug:
        for p in pages:
            if p["slug"] == req_slug or p["pretty_slug"] == req_slug:
                current_nav_title = p["title"]
                break

    # Address helpers
    street  = (settings_obj.address_street or "").strip()
    number  = (settings_obj.address_number or "").strip()
    postal  = (settings_obj.address_postal_code or "").strip()
    city    = (settings_obj.address_city or "").strip()
    country = (settings_obj.address_country or "").strip()

    line1 = " ".join([x for x in [street, number] if x]) if street else ""
    line2 = " ".join([x for x in [postal, city] if x])
    line3 = country
    has_any = any([line1, line2, line3])
    compact = ", ".join([x for x in [line1, line2, line3] if x])

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
