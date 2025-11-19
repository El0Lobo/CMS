"""Synchronize primary/secondary logos to the Assets library."""

from __future__ import annotations

import os

from django.core.files.base import ContentFile

from app.assets.models import Asset, Collection

BRANDING_COLLECTION_SLUG = "site-branding"

LOGO_SPECS = {
    "logo": {
        "slug": "logo-primary",
        "title": "Primary logo",
        "kind": "image",
    },
    "logo_secondary": {
        "slug": "logo-secondary",
        "title": "Secondary logo",
        "kind": "image",
    },
}


def _ensure_collection() -> Collection:
    collection, _ = Collection.objects.get_or_create(
        slug=BRANDING_COLLECTION_SLUG,
        defaults={
            "title": "Site Branding",
            "visibility_mode": "public",
            "description": "Logos uploaded via Setup.",
        },
    )
    updated = False
    if collection.title != "Site Branding":
        collection.title = "Site Branding"
        updated = True
    if collection.visibility_mode != "public":
        collection.visibility_mode = "public"
        updated = True
    if updated:
        collection.save(update_fields=["title", "visibility_mode"])
    return collection


def _write_asset(collection: Collection, attr_name: str, file_field) -> None:
    spec = LOGO_SPECS[attr_name]
    slug = spec["slug"]
    qs = collection.assets.filter(slug=slug)

    if not file_field:
        qs.delete()
        return

    try:
        file_field.open("rb")
        content = file_field.read()
    finally:
        try:
            file_field.close()
        except Exception:  # pragma: no cover
            pass

    if not content:
        qs.delete()
        return

    asset = qs.first()
    if not asset:
        asset = Asset(
            collection=collection,
            slug=slug,
            title=spec["title"],
            visibility="public",
            kind=spec.get("kind", "other"),
            description="Uploaded via Setup",
        )
        asset.save()
    else:
        asset.title = spec["title"]
        asset.visibility = "public"
        asset.kind = spec.get("kind", "other")
        asset.description = "Uploaded via Setup"
        asset.save(update_fields=["title", "visibility", "kind", "description"])

    filename = os.path.basename(file_field.name) or f"{slug}.png"
    asset.file.save(filename, ContentFile(content), save=True)


def sync_branding_assets(settings_obj) -> None:
    """Ensure branding logos are mirrored into the Assets collection."""

    collection = _ensure_collection()

    for attr in LOGO_SPECS:
        file_field = getattr(settings_obj, attr, None)
        _write_asset(collection, attr, file_field)
