from __future__ import annotations

import hashlib
import os
import re
from copy import deepcopy
from typing import TYPE_CHECKING, Any

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from app.setup.models import SiteSettings

if TYPE_CHECKING:
    from collections.abc import Iterable

from . import data_sources

Block = dict[str, Any]
Context = dict[str, Any]

HEX_COLOR_RE = re.compile(r"^#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})$")

STYLE_FONT_STACKS = {
    "sans": '"Inter", "Helvetica Neue", Arial, sans-serif',
    "serif": 'Georgia, "Times New Roman", serif',
    "mono": 'ui-monospace, "SFMono-Regular", Menlo, Consolas, "Liberation Mono", monospace',
    "display": '"Oswald", "Archivo Black", "Arial Narrow", sans-serif',
}

STYLE_FONT_SIZES = {
    "xs": "0.85rem",
    "sm": "0.95rem",
    "base": "1rem",
    "lg": "1.15rem",
    "xl": "1.35rem",
    "xxl": "1.6rem",
}

STYLE_DEFAULTS = {
    "font_family": "",
    "font_size": "",
    "text_color": "",
    "background_color": "",
    "font_asset": None,
}

FONT_MIME_FORMATS = {
    "font/woff2": "woff2",
    "font/woff": "woff",
    "font/ttf": "truetype",
    "font/otf": "opentype",
    "application/font-woff": "woff",
}


def _resolve_media(request, url: str | None) -> str | None:
    if not url:
        return None
    if request and url.startswith("/"):
        return request.build_absolute_uri(url)
    return url


def _clean_hex_color(value: Any) -> str:
    if not isinstance(value, str):
        return ""
    candidate = value.strip()
    if not HEX_COLOR_RE.match(candidate):
        return ""
    if len(candidate) == 4:
        candidate = "#" + "".join(char * 2 for char in candidate[1:])
    return candidate.lower()


def _guess_font_format(url: str, hint: str | None = None) -> str:
    if hint:
        label = hint.lower()
        if label in FONT_MIME_FORMATS.values():
            return label
        mapped = FONT_MIME_FORMATS.get(label)
        if mapped:
            return mapped
    root = url.split("?", 1)[0]
    ext = os.path.splitext(root)[1].lower()
    return {
        ".woff2": "woff2",
        ".woff": "woff",
        ".otf": "opentype",
        ".ttf": "truetype",
    }.get(ext, "truetype")


def _normalise_font_asset(value: Any) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        return None
    url = str(value.get("url") or "").strip()
    if not url or not url.startswith(("/", "http://", "https://")):
        return None
    asset_id = value.get("id")
    try:
        asset_id = int(asset_id)
    except (TypeError, ValueError):
        asset_id = None
    title = str(value.get("title") or "").strip()
    mime = str(value.get("mime_type") or "").strip() or None
    format_hint = str(value.get("format") or "").strip() or None
    return {
        "id": asset_id,
        "title": title,
        "url": url,
        "format": _guess_font_format(url, format_hint or mime),
    }


def _normalise_style_dict(value: Any) -> dict[str, Any]:
    clean = STYLE_DEFAULTS.copy()
    if not isinstance(value, dict):
        return clean
    font_family = value.get("font_family")
    if isinstance(font_family, str) and font_family in STYLE_FONT_STACKS:
        clean["font_family"] = font_family
    font_size = value.get("font_size")
    if isinstance(font_size, str) and font_size in STYLE_FONT_SIZES:
        clean["font_size"] = font_size
    clean["text_color"] = _clean_hex_color(value.get("text_color"))
    clean["background_color"] = _clean_hex_color(value.get("background_color"))
    clean["font_asset"] = _normalise_font_asset(value.get("font_asset"))
    return clean


def _register_font_face(
    asset: dict[str, Any] | None,
    font_cache: dict[str, tuple[str, str]],
) -> str:
    if not asset:
        return ""
    url = asset.get("url")
    if not url:
        return ""
    fmt = asset.get("format") or "truetype"
    family_hint = asset.get("family")
    cache_key = f"{family_hint or url}|{fmt}"
    if cache_key not in font_cache:
        digest = hashlib.sha1(cache_key.encode("utf-8")).hexdigest()[:10]
        family = family_hint or f"CMSFont-{digest}"
        safe_url = url.replace("'", "\\'")
        css = (
            f"@font-face{{font-family:'{family}';src:url('{safe_url}') format('{fmt}');"
            "font-display:swap;}}"
        )
        font_cache[cache_key] = (family, css)
    return font_cache[cache_key][0]


def _build_inline_style(
    style: dict[str, Any],
    font_cache: dict[str, tuple[str, str]],
) -> str:
    inline_parts: list[str] = []
    font_asset = style.get("font_asset")
    font_family_value = ""
    font_face_name = _register_font_face(font_asset, font_cache)
    if font_face_name:
        font_family_value = f"'{font_face_name}'"
    else:
        font_stack = STYLE_FONT_STACKS.get(style.get("font_family") or "")
        if font_stack:
            font_family_value = font_stack
        else:
            style["font_family"] = ""
    if font_family_value:
        inline_parts.append(f"font-family:{font_family_value}")
    size_value = STYLE_FONT_SIZES.get(style.get("font_size") or "")
    if size_value:
        inline_parts.append(f"font-size:{size_value}")
    else:
        style["font_size"] = ""
    if style.get("text_color"):
        inline_parts.append(f"color:{style['text_color']}")
    if style.get("background_color"):
        inline_parts.append(f"background-color:{style['background_color']}")
    return "; ".join(inline_parts)


def _apply_style_overrides(props: dict[str, Any]) -> None:
    font_cache: dict[str, tuple[str, str]] = {}
    base_style = _normalise_style_dict(props.get("style"))
    props["style"] = base_style
    props["style_inline"] = _build_inline_style(base_style, font_cache)

    inline_targets: dict[str, str] = {}
    style_targets = props.get("style_targets")
    if isinstance(style_targets, dict):
        cleaned_targets = {}
        for key, value in style_targets.items():
            style_dict = _normalise_style_dict(value)
            cleaned_targets[key] = style_dict
            inline_targets[key] = _build_inline_style(style_dict, font_cache)
        props["style_targets"] = cleaned_targets
    props["style_inline_targets"] = inline_targets
    inline_fonts = props.get("inline_fonts")
    if isinstance(inline_fonts, list):
        for item in inline_fonts:
            _register_font_face(item, font_cache)
    props["style_font_faces"] = [mark_safe(css) for _, css in font_cache.values()]


def normalise_theme(value: Any) -> dict[str, dict[str, Any]]:
    """
    Normalise a user-supplied theme payload into style dictionaries.
    """

    payload = value if isinstance(value, dict) else {}
    return {
        "body": _normalise_style_dict(payload.get("body")),
        "sections": _normalise_style_dict(payload.get("sections")),
    }


def build_theme_css(value: Any) -> tuple[str, dict[str, dict[str, Any]]]:
    """
    Build inline CSS (including @font-face declarations) for a theme payload.
    """

    theme = normalise_theme(value)
    font_cache: dict[str, tuple[str, str]] = {}
    css_rules: list[str] = []

    body_inline = _build_inline_style(theme["body"], font_cache)
    if body_inline:
        css_rules.append(f"body {{{body_inline}}}")
        css_rules.append(f".site-shell {{{body_inline}}}")
    section_inline = _build_inline_style(theme["sections"], font_cache)
    if section_inline:
        css_rules.append(f".page-block {{{section_inline}}}")
        css_rules.append(f".page-block__container {{{section_inline}}}")

    font_faces = [css for _, css in font_cache.values()]
    css = "\n".join(font_faces + css_rules).strip()
    return css, theme


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
    _apply_style_overrides(props)
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
    "website": "icons/globe.svg",
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


def _social_icon_for(*values: str | None) -> str | None:
    for raw in values:
        if not raw:
            continue
        slug = re.sub(r"[^a-z0-9]+", "", raw.lower())
        if slug.startswith("social"):
            slug = slug.removeprefix("social")
        if slug.endswith("url"):
            slug = slug[: -len("url")]
        if slug in SOCIAL_ICON_FILES:
            return SOCIAL_ICON_FILES[slug]
    return None


def _footer_renderer(*, context: Context, request=None) -> str:
    props = {**context["props"]}
    settings = SiteSettings.get_solo()
    site_context = data_sources.get_site_context()

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
                    "display": item.get("display"),
                    "href": href,
                    "new_tab": bool(item.get("new_tab")),
                    "icon": item.get("icon"),
                }
            )
        return [item for item in normalised if item.get("label") or item.get("href")]

    if not props.get("social_links"):
        socials: list[dict] = []
        for field, label in SOCIAL_FIELD_LABELS:
            url = getattr(settings, field, "")
            if not url:
                continue
            socials.append(
                {
                    "label": label,
                    "href": url,
                    "new_tab": True,
                    "icon": _social_icon_for(field, label),
                }
            )
        props["social_links"] = socials
    else:
        provided: list[dict[str, Any]] = []
        for item in props.get("social_links") or []:
            if not item:
                continue
            icon = item.get("icon") or _social_icon_for(item.get("label"))
            provided.append({**item, "icon": icon})
        props["social_links"] = provided

    props.setdefault("show_language_switcher", True)
    props.setdefault("links_heading", "Explore")
    props.setdefault("legal_heading", "Legal")
    props.setdefault("social_heading", "Connect")

    context = {
        **context,
        "props": props,
        "links": _normalise_links(props.get("links")),
        "legal": _normalise_links(props.get("legal")),
        "social_links": _normalise_links(props.get("social_links")),
        "site": site_context,
        "enabled_languages": settings.get_enabled_languages(),
    }
    return _render_template("pages/blocks/footer.html", context, request=request)


def _gallery_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    items = props.get("items", [])
    for item in items:
        item["image_resolved"] = _resolve_media(request, item.get("image"))
    context = {**context, "items": items}
    return _render_template("pages/blocks/gallery.html", context, request=request)


def _inventory_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    categories = props.get("category_slugs")
    if isinstance(categories, str):
        categories = [slug.strip() for slug in categories.split(",") if slug.strip()]
    items = data_sources.get_public_inventory(categories)
    context = {**context, "items": items, "props": props}
    return _render_template("pages/blocks/inventory.html", context, request=request)


def _map_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    auto_location = props.get("auto_location", True)
    latitude = props.get("latitude")
    longitude = props.get("longitude")
    lat_value: float | None
    lon_value: float | None
    try:
        lat_value = float(latitude) if latitude not in (None, "") else None
    except (TypeError, ValueError):
        lat_value = None
    try:
        lon_value = float(longitude) if longitude not in (None, "") else None
    except (TypeError, ValueError):
        lon_value = None
    try:
        zoom = int(props.get("zoom") or 15)
    except (TypeError, ValueError):
        zoom = 15
    block = context.get("block") or {}
    map_id = f"page-map-{block.get('id', 'map')}"
    site = data_sources.get_site_context()
    address_override = (props.get("address_override") or "").strip()
    if address_override:
        search_address = address_override
    else:
        addr = site.get("address") or {}
        parts = []
        line1 = " ".join(filter(None, [addr.get("street"), addr.get("number")])).strip()
        if line1:
            parts.append(line1)
        line2 = " ".join(filter(None, [addr.get("postal_code"), addr.get("city")])).strip()
        if line2:
            parts.append(line2)
        if addr.get("country"):
            parts.append(addr.get("country"))
        search_address = ", ".join(parts)

    def _clean_items(values):
        cleaned: list[dict[str, str]] = []
        for item in values or []:
            if not isinstance(item, dict):
                continue
            label = str(item.get("label") or "").strip()
            details = str(item.get("details") or "").strip()
            if not label and not details:
                continue
            cleaned.append({"label": label, "details": details})
        return cleaned

    context = {
        **context,
        "map_id": map_id,
        "latitude": lat_value,
        "longitude": lon_value,
        "zoom": zoom,
        "transport_items": _clean_items(props.get("transport_items")),
        "parking_items": _clean_items(props.get("parking_items")),
        "auto_location": bool(auto_location),
        "address_search": search_address,
    }
    return _render_template("pages/blocks/map.html", context, request=request)


def _navigation_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    from .navigation import build_nav_payload, get_navigation_entries, serialize_nav_entries

    if props.get("enabled") is False:
        return ""
    site = data_sources.get_site_context()
    logo_source = props.get("logo_image") or site.get("logo")
    logo = _resolve_media(request, logo_source)
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
    "inventory": _inventory_renderer,
    "navigation": _navigation_renderer,
    "map": _map_renderer,
}
