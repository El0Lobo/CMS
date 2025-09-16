from django.db import migrations

def seed_units_and_roots(apps, schema_editor):
    Unit = apps.get_model('menu', 'Unit')
    Category = apps.get_model('menu', 'Category')

    units = [
        ("L", "Liters", "volume"),
        ("mL", "Milliliters", "volume"),
        ("g", "Grams", "mass"),
        ("pcs", "Pieces", "count"),
    ]
    for code, display, kind in units:
        Unit.objects.get_or_create(code=code, defaults={"display": display, "kind": kind})

    # Roots
    drinks, _ = Category.objects.get_or_create(slug="drinks", defaults={"name": "Drinks", "kind": "drink", "parent": None})
    food, _ = Category.objects.get_or_create(slug="food", defaults={"name": "Food", "kind": "food", "parent": None})

    # Default subcategories for drinks
    non_alc, _ = Category.objects.get_or_create(slug="non-alcoholic", defaults={"name": "Non-alcoholic", "kind": "drink", "parent": drinks})
    alc, _ = Category.objects.get_or_create(slug="alcoholic", defaults={"name": "Alcoholic", "kind": "drink", "parent": drinks})

def unseed(apps, schema_editor):
    # keep data
    pass

class Migration(migrations.Migration):
    dependencies = [('menu', '0001_initial')]
    operations = [migrations.RunPython(seed_units_and_roots, unseed)]
