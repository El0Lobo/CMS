from __future__ import annotations

from typing import Any, Dict, Optional

from django.http import HttpRequest

from .models import Page


def media_url(request: Optional[HttpRequest], field) -> Optional[str]:
    if not field:
        return None
    url = getattr(field, "url", None)
    if not url:
        return None
    if request and url.startswith("/"):
        return request.build_absolute_uri(url)
    return url


def serialize_page(page: Page, request: Optional[HttpRequest] = None) -> Dict[str, Any]:
    return {
        "id": page.pk,
        "title": page.title,
        "slug": page.slug,
        "summary": page.summary,
        "status": page.status,
        "is_visible": page.is_visible,
        "show_navigation_bar": page.show_navigation_bar,
        "render_body_only": page.render_body_only,
        "navigation_order": page.navigation_order,
        "custom_nav_items": page.custom_nav_items or [],
        "hero_image": media_url(request, getattr(page, "hero_image", None)),
        "body": page.body,
        "blocks": page.blocks or [],
        "created_at": page.created_at.isoformat() if page.created_at else None,
        "updated_at": page.updated_at.isoformat() if page.updated_at else None,
        "published_at": page.published_at.isoformat() if page.published_at else None,
    }
