from django.db import migrations
from django.utils.text import slugify


def normalise_nav_items(apps, schema_editor):
    Page = apps.get_model("pages", "Page")
    for page in Page.objects.exclude(custom_nav_items=None):
        items = page.custom_nav_items or []
        if not isinstance(items, list):
            continue
        changed = False
        cleaned = []
        for slug in items:
            if not isinstance(slug, str):
                continue
            slug_norm = slugify(slug) or slug.strip()
            if slug_norm == "__login":
                slug_norm = "login"
            if not slug_norm:
                continue
            if slug_norm not in cleaned:
                cleaned.append(slug_norm)
            if slug_norm != slug:
                changed = True
        if changed:
            page.custom_nav_items = cleaned
            page.save(update_fields=["custom_nav_items"])


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0008_remove_page_login_link_fields"),
    ]

    operations = [
        migrations.RunPython(normalise_nav_items, migrations.RunPython.noop),
    ]
