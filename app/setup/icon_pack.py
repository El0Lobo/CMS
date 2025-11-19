"""Helpers for importing a site icon pack into the Assets module."""

from __future__ import annotations

import io
import os
import zipfile
from typing import Dict, Iterable

from django.core.files.base import ContentFile
from django.db import transaction

from app.assets.models import Asset, Collection

ICON_COLLECTION_SLUG = "site-icons"

# filename (lowercase) -> metadata about how to store/use it
ICON_FILE_SPECS: Dict[str, Dict[str, str]] = {
    "favicon.ico": {
        "slug": "favicon-ico",
        "title": "Favicon (ICO)",
        "kind": "image",
        "mime": "image/x-icon",
        "link": {"rel": "icon", "type": "image/x-icon"},
    },
    "favicon.svg": {
        "slug": "favicon-svg",
        "title": "Favicon (SVG)",
        "kind": "image",
        "mime": "image/svg+xml",
        "link": {"rel": "icon", "type": "image/svg+xml"},
    },
    "apple-touch-icon.png": {
        "slug": "apple-touch-icon",
        "title": "Apple touch icon",
        "kind": "image",
        "mime": "image/png",
        "link": {"rel": "apple-touch-icon", "sizes": "180x180", "type": "image/png"},
    },
    "favicon-96x96.png": {
        "slug": "favicon-96",
        "title": "Favicon 96×96",
        "kind": "image",
        "mime": "image/png",
        "link": {"rel": "icon", "sizes": "96x96", "type": "image/png"},
    },
    "web-app-manifest-192x192.png": {
        "slug": "manifest-icon-192",
        "title": "Web app icon 192×192",
        "kind": "image",
        "mime": "image/png",
        "link": {"rel": "icon", "sizes": "192x192", "type": "image/png"},
    },
    "web-app-manifest-512x512.png": {
        "slug": "manifest-icon-512",
        "title": "Web app icon 512×512",
        "kind": "image",
        "mime": "image/png",
        "link": {"rel": "icon", "sizes": "512x512", "type": "image/png"},
    },
    "site.webmanifest": {
        "slug": "site-manifest",
        "title": "Web app manifest",
        "kind": "other",
        "mime": "application/manifest+json",
        "link": {"rel": "manifest"},
    },
}


class IconPackError(Exception):
    """Raised when an uploaded icon pack cannot be processed."""


def _normalise_members(members: Iterable[str]) -> Dict[str, str]:
    result: Dict[str, str] = {}
    for name in members:
        if name.endswith("/"):
            continue
        base = os.path.basename(name).lower()
        if base and base not in result:
            result[base] = name
    return result


def _ensure_collection() -> Collection:
    collection, _ = Collection.objects.get_or_create(
        slug=ICON_COLLECTION_SLUG,
        defaults={
            "title": "Site Icons",
            "visibility_mode": "public",
            "description": "Uploaded icon pack (favicons/web manifest).",
        },
    )
    needs_update = False
    if collection.title != "Site Icons":
        collection.title = "Site Icons"
        needs_update = True
    if collection.visibility_mode != "public":
        collection.visibility_mode = "public"
        needs_update = True
    if needs_update:
        collection.save(update_fields=["title", "visibility_mode"])
    return collection


def import_icon_pack(uploaded_file) -> None:
    """
    Store the uploaded ZIP as a dedicated collection of Asset objects.
    Existing icon assets are removed before the new ones are stored.
    """

    if not uploaded_file:
        return

    try:
        uploaded_file.seek(0)
    except (AttributeError, OSError):
        pass

    data = uploaded_file.read()
    if not data:
        raise IconPackError("Uploaded file is empty.")

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            members = _normalise_members(zf.namelist())
            missing = [name for name in ICON_FILE_SPECS if name not in members]
            if missing:
                raise IconPackError(
                    "Icon pack is missing required files: " + ", ".join(missing)
                )

            collection = _ensure_collection()
            with transaction.atomic():
                collection.assets.all().delete()

                for filename, meta in ICON_FILE_SPECS.items():
                    zip_path = members[filename]
                    content = zf.read(zip_path)
                    if not content:
                        raise IconPackError(f"{filename} is empty in the ZIP.")

                    asset = Asset(
                        collection=collection,
                        title=meta["title"],
                        slug=meta["slug"],
                        visibility="public",
                        kind=meta.get("kind") or "other",
                        mime_type=meta.get("mime") or "",
                        appears_on="site-icons",
                        description="Auto-uploaded icon",
                    )
                    asset.save()
                    ext = os.path.splitext(filename)[1] or ""
                    file_name = f"{meta['slug']}{ext}"
                    asset.file.save(file_name, ContentFile(content), save=True)
    except IconPackError:
        raise
    except zipfile.BadZipFile as exc:
        raise IconPackError("Upload is not a valid ZIP archive.") from exc
    except Exception as exc:  # pragma: no cover - defensive
        raise IconPackError("Could not process the uploaded icon pack.") from exc
