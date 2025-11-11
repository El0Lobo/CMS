from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from django.urls import reverse
from django.utils.text import slugify

from app.setup.models import SiteSettings

from .models import Page


@dataclass
class NavEntry:
    title: str
    slug: str
    url: str
    pretty_slug: str
    pretty_url: str


def _parse_required_lines(lines: Iterable[str]) -> List[Tuple[str, str]]:
    parsed: List[Tuple[str, str]] = []
    seen: set[str] = set()
    for raw in lines:
        if not raw:
            continue
        slug = ""
        title = ""
        if "|" in raw:
            slug_part, title_part = raw.split("|", 1)
            slug = slugify(slug_part.strip()) if slug_part.strip() else ""
            title = title_part.strip() or slug
        else:
            title = raw.strip()
            slug = slugify(title)
        slug = slug or "page"
        title = title or slug
        if slug in seen:
            continue
        seen.add(slug)
        parsed.append((slug, title))
    return parsed


def ensure_pages_from_settings(settings_obj: Optional[SiteSettings] = None) -> None:
    """
    Ensure each entry listed in SiteSettings.required_pages has a Page record.
    """

    if settings_obj is None:
        settings_obj = SiteSettings.get_solo()

    raw_lines = [
        line.strip()
        for line in (settings_obj.required_pages or "").splitlines()
        if line.strip()
    ]
    parsed = _parse_required_lines(raw_lines)

    for order, (slug, title) in enumerate(parsed):
        Page.objects.get_or_create(
            slug=slug,
            defaults={
                "title": title,
                "status": Page.Status.PUBLISHED,
                "is_visible": True,
                "show_in_navigation": True,
                "navigation_order": order,
            },
        )


def get_navigation_entries(*, include_hidden: bool = False) -> List[NavEntry]:
    """
    Return the list of navigation entries sourced from published Page objects,
    falling back to SiteSettings.required_pages if no pages exist.
    """

    pages_qs = Page.objects.filter(status=Page.Status.PUBLISHED)
    if not include_hidden:
        pages_qs = pages_qs.filter(is_visible=True, show_in_navigation=True)
    pages_qs = pages_qs.order_by("navigation_order", "title")

    entries: List[NavEntry] = []
    for page in pages_qs:
        slug = page.slug
        url = page.get_absolute_url()
        pretty_slug = slugify(page.title) or slug
        pretty_url = "/" if pretty_slug == "home" else f"/{pretty_slug}/"
        entries.append(
            NavEntry(
                title=page.title,
                slug=slug,
                url=url,
                pretty_slug=pretty_slug,
                pretty_url=pretty_url,
            )
        )

    if entries:
        return entries

    # fallback to SiteSettings.required_pages for legacy installs
    settings_obj = SiteSettings.get_solo()
    ensure_pages_from_settings(settings_obj)

    parsed = _parse_required_lines(
        [
            line.strip()
            for line in (settings_obj.required_pages or "").splitlines()
            if line.strip()
        ]
    )

    fallback: List[NavEntry] = []
    for slug, title in parsed:
        try:
            url = reverse("public:page-detail", kwargs={"slug": slug})
        except Exception:
            url = "/" if slug == "home" else f"/{slug}/"
        pretty_slug = slugify(title) or slug
        pretty_url = "/" if pretty_slug == "home" else f"/{pretty_slug}/"
        fallback.append(
            NavEntry(
                title=title,
                slug=slug,
                url=url,
                pretty_slug=pretty_slug,
                pretty_url=pretty_url,
            )
        )
    return fallback
