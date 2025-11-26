from __future__ import annotations

from copy import deepcopy
import re
from typing import TYPE_CHECKING, Any

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from app.setup.models import SiteSettings

if TYPE_CHECKING:
    from collections.abc import Iterable

from . import data_sources

Block = dict[str, Any]
Context = dict[str, Any]


def _resolve_media(request, url: str | None) -> str | None:
    if not url:
        return None
    if request and url.startswith("/"):
        return request.build_absolute_uri(url)
    return url


def render_blocks(
    blocks: Iterable[Block],
    *,
    request=None,
    extra_context: Context | None = None,
) -> str:
    rendered: list[str] = []
    for block in blocks or []:
        html = render_block(block, request=request, extra_context=extra_context)
        if html:
            rendered.append(html)
    return mark_safe("".join(rendered))  # noqa: S308


def render_block(
    block: Block,
    *,
    request=None,
    extra_context: Context | None = None,
) -> str:
    block_type = block.get("type")
    renderer = BLOCK_RENDERERS.get(block_type)
    if not renderer:
        return ""
    props = deepcopy(block.get("props", {}))
    context = {
        "block": block,
        "props": props,
        **(extra_context or {}),
    }
    return renderer(context=context, request=request)


def _render_template(template_name: str, context: Context, request=None) -> str:
    return render_to_string(template_name, context, request=request)


def _hero_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    props["background_image_resolved"] = _resolve_media(request, props.get("background_image"))
    props.setdefault("alignment", "center")
    props.setdefault("overlay", 0.4)
    props.setdefault("actions", [])
    return _render_template("pages/blocks/hero.html", context, request=request)


def _rich_text_renderer(*, context: Context, request=None) -> str:
    return _render_template("pages/blocks/rich_text.html", context, request=request)


def _events_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    events = data_sources.get_events(
        limit=int(props.get("limit", 6) or 6),
        include_internal=bool(props.get("include_internal")),
    )
    for event in events:
        event["hero_image"] = _resolve_media(request, event.get("hero_image"))
        if request and event.get("url") and event["url"].startswith("/"):
            event["url"] = request.build_absolute_uri(event["url"])
    context = {**context, "events": events}
    return _render_template("pages/blocks/events.html", context, request=request)


def _menu_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    categories = data_sources.get_menu_structure(props.get("category_slugs"))
    context = {**context, "categories": categories}
    return _render_template("pages/blocks/menu.html", context, request=request)


def _opening_hours_renderer(*, context: Context, request=None) -> str:
    site = data_sources.get_site_context()
    context = {**context, "site": site, "hours": site["opening_hours"]}
    return _render_template("pages/blocks/opening_hours.html", context, request=request)


def _contact_renderer(*, context: Context, request=None) -> str:
    site = data_sources.get_site_context()
    site["logo"] = _resolve_media(request, site.get("logo"))
    props = context.get("props", {})
    site_contact = site.get("contact", {}) or {}
    site_address = site.get("address", {}) or {}
    site_social = site.get("social", {}) or {}

    default_contact_fields = [field for field, _ in CONTACT_BLOCK_FIELDS]
    selected_contact_fields = props.get("contact_fields")
    if isinstance(selected_contact_fields, list):
        selected_contact_fields = [
            field for field in selected_contact_fields if field in default_contact_fields
        ]
    else:
        selected_contact_fields = default_contact_fields

    social_defaults = [field for field, _ in CONTACT_BLOCK_SOCIALS]
    selected_social_fields = props.get("social_fields")
    if isinstance(selected_social_fields, list):
        selected_social_fields = [
            field for field in selected_social_fields if field in social_defaults
        ]
    else:
        selected_social_fields = social_defaults if props.get("show_social", True) else []

    def _clean_url(value: str | None) -> str:
        if not value:
            return ""
        value = re.sub(r"^https?://", "", value)
        return value.rstrip("/")

    if site_contact.get("website"):
        site_contact["website_display"] = _clean_url(site_contact.get("website"))

    social_links: list[dict[str, str]] = []
    for key, label in CONTACT_BLOCK_SOCIALS:
        if key not in selected_social_fields:
            continue
        url = site_social.get(key)
        if not url:
            continue
        social_links.append(
            {
                "label": label,
                "href": url,
                "display": _clean_url(url),
                "icon": SOCIAL_ICON_FILES.get(key),
            }
        )

    address_has_any = any(
        [
            site_address.get("street"),
            site_address.get("number"),
            site_address.get("postal_code"),
            site_address.get("city"),
            site_address.get("country"),
        ]
    )

    show_address = "address" in selected_contact_fields and address_has_any
    show_phone = "phone" in selected_contact_fields and bool(site_contact.get("phone"))
    show_email = "email" in selected_contact_fields and bool(site_contact.get("email"))
    show_website = "website" in selected_contact_fields and bool(site_contact.get("website"))

    context = {
        **context,
        "site": site,
        "contact_fields": selected_contact_fields,
        "social_links": social_links,
        "show_address": show_address,
        "show_phone": show_phone,
        "show_email": show_email,
        "show_website": show_website,
        "contact_icons": CONTACT_ICON_FILES,
    }
    return _render_template("pages/blocks/contact.html", context, request=request)


SOCIAL_FIELD_LABELS = [
    ("social_instagram", "Instagram"),
    ("social_facebook", "Facebook"),
    ("social_twitter", "Twitter"),
    ("social_tiktok", "TikTok"),
    ("social_youtube", "YouTube"),
    ("social_spotify", "Spotify"),
    ("social_soundcloud", "SoundCloud"),
    ("social_bandcamp", "Bandcamp"),
    ("social_linkedin", "LinkedIn"),
    ("social_mastodon", "Mastodon"),
    ("website_url", "Website"),
]

CONTACT_BLOCK_FIELDS = [
    ("address", "Address"),
    ("phone", "Phone"),
    ("email", "Email"),
    ("website", "Website"),
]

CONTACT_BLOCK_SOCIALS = [
    ("facebook", "Facebook"),
    ("instagram", "Instagram"),
    ("twitter", "Twitter"),
    ("tiktok", "TikTok"),
    ("youtube", "YouTube"),
    ("spotify", "Spotify"),
    ("soundcloud", "SoundCloud"),
    ("bandcamp", "Bandcamp"),
    ("linkedin", "LinkedIn"),
    ("mastodon", "Mastodon"),
]

CONTACT_ICON_FILES = {
    "address": "icons/home.svg",
    "phone": "icons/phone.svg",
    "email": "icons/email.svg",
    "website": "icons/globe.svg",
}

SOCIAL_ICON_FILES = {
    "facebook": "icons/facebook.svg",
    "instagram": "icons/instagram.svg",
    "twitter": "icons/twitter.svg",
    "tiktok": "icons/tiktok.svg",
    "youtube": "icons/youtube.svg",
    "spotify": "icons/spotify.svg",
    "soundcloud": "icons/soundcloud.svg",
    "bandcamp": "icons/bandcamp.svg",
    "linkedin": "icons/linkedin.svg",
    "mastodon": "icons/mastodon.svg",
}


def _format_address(settings: SiteSettings) -> str:
    lines: list[str] = []
    street = " ".join(filter(None, [settings.address_street, settings.address_number])).strip()
    if street:
        lines.append(street)
    city_line = " ".join(
        filter(None, [settings.address_postal_code, settings.address_city])
    ).strip()
    if city_line:
        lines.append(city_line)
    if settings.address_country:
        lines.append(settings.address_country)
    return "\n".join(lines)


def _footer_renderer(*, context: Context, request=None) -> str:
    props = {**context["props"]}
    settings = SiteSettings.get_solo()

    if not props.get("brand_name"):
        props["brand_name"] = settings.org_name
    if not props.get("brand_tagline") and settings.mode:
        props["brand_tagline"] = settings.get_mode_display()

    logo = props.get("brand_logo")
    if not logo and settings.logo:
        try:
            logo = settings.logo.url
        except Exception:
            logo = None
    props["brand_logo_resolved"] = _resolve_media(request, logo)

    if not props.get("address_html"):
        props["address_html"] = _format_address(settings)

    def _normalise_links(items):
        normalised = []
        for item in items or []:
            if not item:
                continue
            href = item.get("href")
            if href and request and href.startswith("/"):
                href = request.build_absolute_uri(href)
            normalised.append(
                {
                    "label": item.get("label"),
                    "href": href,
                    "new_tab": bool(item.get("new_tab")),
                }
            )
        return [item for item in normalised if item.get("label") or item.get("href")]

    if not props.get("social_links"):
        socials: list[dict] = []
        for field, label in SOCIAL_FIELD_LABELS:
            url = getattr(settings, field, "")
            if url:
                socials.append({"label": label, "href": url, "new_tab": True})
        props["social_links"] = socials

    context = {
        **context,
        "props": props,
        "links": _normalise_links(props.get("links")),
        "legal": _normalise_links(props.get("legal")),
        "social_links": _normalise_links(props.get("social_links")),
    }
    return _render_template("pages/blocks/footer.html", context, request=request)


def _gallery_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    items = props.get("items", [])
    for item in items:
        item["image_resolved"] = _resolve_media(request, item.get("image"))
    context = {**context, "items": items}
    return _render_template("pages/blocks/gallery.html", context, request=request)


def _navigation_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    from .navigation import build_nav_payload, get_navigation_entries, serialize_nav_entries

    site = data_sources.get_site_context()
    logo = _resolve_media(request, site.get("logo"))
    override_links = props.get("links") or context.get("nav_override") or []
    if override_links:
        nav_entries = build_nav_payload(override_links)
    else:
        nav_entries = serialize_nav_entries(get_navigation_entries())
    enabled_languages = SiteSettings.get_solo().get_enabled_languages()
    context = {
        **context,
        "props": props,
        "site": site,
        "logo": logo,
        "nav_items": nav_entries,
        "enabled_languages": enabled_languages,
    }
    return _render_template("pages/blocks/navigation.html", context, request=request)


BLOCK_RENDERERS = {
    "hero": _hero_renderer,
    "rich_text": _rich_text_renderer,
    "events": _events_renderer,
    "menu": _menu_renderer,
    "opening_hours": _opening_hours_renderer,
    "contact": _contact_renderer,
    "footer": _footer_renderer,
    "gallery": _gallery_renderer,
    "navigation": _navigation_renderer,
}
