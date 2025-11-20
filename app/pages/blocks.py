from __future__ import annotations

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


def _render_template(template_name: str, context: Context) -> str:
    return render_to_string(template_name, context)


def _hero_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    props["background_image_resolved"] = _resolve_media(request, props.get("background_image"))
    props.setdefault("alignment", "center")
    props.setdefault("overlay", 0.4)
    props.setdefault("actions", [])
    return _render_template("pages/blocks/hero.html", context)


def _rich_text_renderer(*, context: Context, request=None) -> str:
    return _render_template("pages/blocks/rich_text.html", context)


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
    return _render_template("pages/blocks/events.html", context)


def _menu_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    categories = data_sources.get_menu_structure(props.get("category_slugs"))
    context = {**context, "categories": categories}
    return _render_template("pages/blocks/menu.html", context)


def _opening_hours_renderer(*, context: Context, request=None) -> str:
    site = data_sources.get_site_context()
    context = {**context, "site": site, "hours": site["opening_hours"]}
    return _render_template("pages/blocks/opening_hours.html", context)


def _contact_renderer(*, context: Context, request=None) -> str:
    site = data_sources.get_site_context()
    site["logo"] = _resolve_media(request, site.get("logo"))
    context = {**context, "site": site}
    return _render_template("pages/blocks/contact.html", context)


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
    return _render_template("pages/blocks/footer.html", context)


def _gallery_renderer(*, context: Context, request=None) -> str:
    props = context["props"]
    items = props.get("items", [])
    for item in items:
        item["image_resolved"] = _resolve_media(request, item.get("image"))
    context = {**context, "items": items}
    return _render_template("pages/blocks/gallery.html", context)


BLOCK_RENDERERS = {
    "hero": _hero_renderer,
    "rich_text": _rich_text_renderer,
    "events": _events_renderer,
    "menu": _menu_renderer,
    "opening_hours": _opening_hours_renderer,
    "contact": _contact_renderer,
    "footer": _footer_renderer,
    "gallery": _gallery_renderer,
}
