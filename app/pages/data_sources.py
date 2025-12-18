from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import DateTimeField, Prefetch
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.utils.html import strip_tags

from app.assets.models import Asset
from app.events.models import Event
from app.inventory.models import InventoryItem
from app.menu.models import Category, Item
from app.setup.models import SiteSettings
from app.news.models import NewsPost

if TYPE_CHECKING:
    from collections.abc import Sequence
    from decimal import Decimal

WEEKDAY_LABELS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def _iso_datetime(value):
    if not value:
        return None
    if timezone.is_aware(value):
        value = timezone.localtime(value)
    return value.isoformat()


def _decimal_to_str(value: Decimal | None) -> str | None:
    if value is None:
        return None
    return format(value, "f")


def get_events(limit: int = 6, *, include_internal: bool = False) -> list[dict[str, Any]]:
    """Return upcoming events for use in blocks."""

    limit = max(1, min(limit, 50))
    now = timezone.now()

    queryset = (
        Event.objects.filter(status=Event.Status.PUBLISHED)
        .annotate(
            effective_start=Coalesce(
                "recurrence_next_start_at",
                "starts_at",
                output_field=DateTimeField(),
            )
        )
        .filter(effective_start__isnull=False, effective_start__gte=now)
        .order_by("effective_start")
        .prefetch_related("categories")
    )
    if not include_internal:
        queryset = queryset.filter(event_type=Event.EventType.PUBLIC)

    events: list[dict[str, Any]] = []
    for event in queryset[:limit]:
        categories = [cat.name for cat in event.categories.all()]
        events.append(
            {
                "title": event.title,
                "slug": event.slug,
                "teaser": event.teaser,
                "event_type": event.event_type,
                "starts_at": _iso_datetime(event.starts_at),
                "doors_at": _iso_datetime(event.doors_at),
                "ends_at": _iso_datetime(event.ends_at),
                "curfew_at": _iso_datetime(event.curfew_at),
                "effective_start": _iso_datetime(event.recurrence_next_start_at or event.starts_at),
                "recurrence": {
                    "frequency": event.recurrence_frequency,
                    "description": event.recurrence_description,
                    "next_start": _iso_datetime(event.recurrence_next_start_at),
                },
                "hero_image": event.hero_image.url if event.hero_image else None,
                "ticket_url": event.ticket_url,
                "ticket_price_from": _decimal_to_str(event.ticket_price_from),
                "ticket_price_to": _decimal_to_str(event.ticket_price_to),
                "is_free": event.is_free,
                "featured": event.featured,
                "description": event.description_public,
                "categories": categories,
                "url": event.get_absolute_url(),
            }
        )

    return events


def _serialize_menu_category(category: Category, *, depth: int = 0) -> dict[str, Any]:
    children = [
        _serialize_menu_category(child, depth=depth + 1) for child in category.children.all()
    ]
    items = []
    for item in category.items.all():
        if isinstance(item, Item) and not item.visible_public:
            continue
        items.append(
            {
                "name": item.name,
                "slug": item.slug,
                "description": item.description,
                "allergens": item.allergens_note,
                "flags": {
                    "vegan": item.vegan,
                    "vegetarian": item.vegetarian,
                    "gluten_free": item.gluten_free,
                    "sugar_free": item.sugar_free,
                    "lactose_free": item.lactose_free,
                    "nut_free": item.nut_free,
                    "halal": item.halal,
                    "kosher": item.kosher,
                },
                "status": {
                    "featured": item.featured,
                    "sold_out_until": _iso_datetime(item.sold_out_until),
                    "new_until": _iso_datetime(item.new_until),
                    "is_sold_out": item.is_sold_out(),
                    "is_new": item.is_new(),
                },
                "variants": [
                    {
                        "label": variant.label,
                        "quantity": float(variant.quantity),
                        "unit": variant.unit.code,
                        "price": _decimal_to_str(variant.price),
                        "abv": _decimal_to_str(variant.abv),
                    }
                    for variant in item.variants.all()
                ],
            }
        )
    return {
        "name": category.name,
        "slug": category.slug,
        "kind": category.kind,
        "depth": depth,
        "items": items,
        "children": children,
    }


def get_menu_structure(category_slugs: Sequence[str] | None = None) -> list[dict[str, Any]]:
    """Return structured menu data optionally filtered by category slugs."""

    base_qs = Category.objects.prefetch_related(
        Prefetch(
            "children",
            queryset=Category.objects.all().prefetch_related(
                "children",
                "items__variants",
            ),
        ),
        "items__variants",
    ).order_by("name")

    if category_slugs:
        base_qs = base_qs.filter(slug__in=category_slugs)
    else:
        base_qs = base_qs.filter(parent__isnull=True)

    return [_serialize_menu_category(cat, depth=0) for cat in base_qs]


def get_recent_news(limit: int = 3, category: str | None = None) -> list[dict[str, Any]]:
    queryset = NewsPost.objects.published().public()
    if category:
        queryset = queryset.filter(category__iexact=category)
    posts: list[dict[str, Any]] = []
    for post in queryset[: max(1, min(limit, 12))]:
        summary = post.summary or strip_tags(post.body or "")
        timestamp = post.display_timestamp
        iso_value = _iso_datetime(timestamp)
        if timestamp and timezone.is_naive(timestamp):
            timestamp = timezone.make_aware(timestamp)
        display_label = (
            timezone.localtime(timestamp).strftime("%b %d, %Y") if timestamp else ""
        )
        posts.append(
            {
                "title": post.title,
                "summary": summary[:220],
                "category": post.category,
                "published_at": iso_value,
                "display_date": display_label,
                "url": post.get_absolute_url(),
            }
        )
    return posts


def get_news_categories() -> list[str]:
    return list(
        NewsPost.objects.published()
        .public()
        .exclude(category="")
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )


def _serialize_opening_hours(settings: SiteSettings) -> list[dict[str, Any]]:
    hours = []
    for entry in settings.hours.order_by("weekday"):
        label = (
            entry.get_weekday_display()
            if hasattr(entry, "get_weekday_display")
            else WEEKDAY_LABELS[entry.weekday]
        )
        if entry.closed:
            hours.append({"weekday": label, "closed": True})
        else:
            hours.append(
                {
                    "weekday": label,
                    "closed": False,
                    "open_time": entry.open_time.strftime("%H:%M") if entry.open_time else None,
                    "close_time": entry.close_time.strftime("%H:%M") if entry.close_time else None,
                }
            )
    return hours


def get_site_context() -> dict[str, Any]:
    settings = SiteSettings.get_solo()
    return {
        "name": settings.org_name,
        "logo": settings.logo.url if settings.logo else None,
        "address": {
            "street": settings.address_street,
            "number": settings.address_number,
            "postal_code": settings.address_postal_code,
            "city": settings.address_city,
            "country": settings.address_country,
        },
        "contact": {
            "email": settings.contact_email,
            "phone": settings.contact_phone,
            "website": settings.website_url,
        },
        "social": {
            "facebook": settings.social_facebook,
            "instagram": settings.social_instagram,
            "twitter": settings.social_twitter,
            "tiktok": settings.social_tiktok,
            "youtube": settings.social_youtube,
            "spotify": settings.social_spotify,
            "soundcloud": settings.social_soundcloud,
            "bandcamp": settings.social_bandcamp,
            "linkedin": settings.social_linkedin,
            "mastodon": settings.social_mastodon,
        },
        "policies": {
            "smoking_allowed": settings.smoking_allowed,
            "pets_allowed_text": settings.pets_allowed_text,
            "typical_age_range": settings.typical_age_range,
            "minors_policy_note": settings.minors_policy_note,
            "awareness_team_available": settings.awareness_team_available,
            "awareness_contact": settings.awareness_contact,
            "lgbtq_friendly": settings.lgbtq_friendly,
        },
        "opening_hours": {
            "publish": settings.publish_opening_times,
            "entries": _serialize_opening_hours(settings),
        },
        "same_as": [line.strip() for line in (settings.same_as or "").splitlines() if line.strip()],
        "geo": {
            "lat": float(settings.geo_lat) if settings.geo_lat is not None else None,
            "lng": float(settings.geo_lng) if settings.geo_lng is not None else None,
        },
        "price_range": settings.price_range,
        "default_currency": settings.default_currency,
    }


def get_public_inventory(category_slugs: list[str] | None = None) -> list[dict[str, Any]]:
    qs = InventoryItem.objects.filter(public_visible=True, is_active=True)
    if category_slugs:
        qs = qs.filter(category__slug__in=category_slugs)
    items = []
    for item in qs.order_by("name"):
        items.append(
            {
                "name": item.name,
                "description": item.public_description or item.description,
                "url": item.public_url,
                "category": item.category.name if item.category else "",
            }
        )
    return items


def _serialise_asset(asset: Asset) -> dict[str, Any] | None:
    url = asset.file.url if asset.file else asset.url
    if not url:
        return None
    collection = asset.collection
    return {
        "id": asset.pk,
        "title": asset.title,
        "slug": asset.slug,
        "kind": asset.kind,
        "description": asset.description,
        "url": url,
        "mime_type": asset.mime_type,
        "size_bytes": asset.size_bytes,
        "width": asset.width,
        "height": asset.height,
        "duration_seconds": asset.duration_seconds,
        "collection": {
            "id": collection.pk if collection else None,
            "title": collection.title if collection else None,
        },
        "is_external": asset.is_external,
        "external_domain": asset.external_domain,
    }


def get_public_assets(kinds: Sequence[str] | None = None) -> list[dict[str, Any]]:
    """
    Return public assets filtered by kind for use in page builder blocks.
    """

    qs = Asset.objects.select_related("collection").all()
    if kinds:
        qs = qs.filter(kind__in=kinds)

    results: list[dict[str, Any]] = []
    for asset in qs:
        collection = asset.collection
        effective_visibility = asset.effective_visibility
        if effective_visibility != "public":
            continue

        payload = _serialise_asset(asset)
        if payload:
            results.append(payload)

    return results


def get_public_assets_by_ids(ids: Sequence[int] | None) -> dict[int, dict[str, Any]]:
    """
    Return a mapping of asset ID -> payload for the requested public assets.
    """

    if not ids:
        return {}
    qs = Asset.objects.select_related("collection").filter(pk__in=ids)
    results: dict[int, dict[str, Any]] = {}
    for asset in qs:
        if asset.effective_visibility != "public":
            continue
        payload = _serialise_asset(asset)
        if payload:
            results[asset.pk] = payload
    return results
