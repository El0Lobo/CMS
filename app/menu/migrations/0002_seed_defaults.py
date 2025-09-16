# app/menu/migrations/0002_seed_defaults.py
from django.db import migrations

def seed(apps, schema_editor):
    Unit = apps.get_model('menu', 'Unit')
    Category = apps.get_model('menu', 'Category')

    # Units
    units = [
        # volume
        ('l',   'liter',  'volume'),
        ('ml',  'milliliter', 'volume'),
        # mass
        ('g',   'gram',   'mass'),
        ('kg',  'kilogram','mass'),
        # count
        ('pc',  'piece',  'count'),
    ]
    for code, display, kind in units:
        Unit.objects.get_or_create(code=code, defaults={'display': display, 'kind': kind})

    # Top categories
    drinks, _ = Category.objects.get_or_create(
        slug='drinks',
        defaults={'name': 'Drinks', 'kind': 'drink', 'parent': None}
    )
    food, _ = Category.objects.get_or_create(
        slug='food',
        defaults={'name': 'Food', 'kind': 'food', 'parent': None}
    )

    # Example subcategory under Drinks
    Category.objects.get_or_create(
        slug='non-alcoholic',
        defaults={'name': 'Non-alcoholic', 'kind': 'drink', 'parent': drinks}
    )

def unseed(apps, schema_editor):
    # Keep it simple: don’t delete on reverse, to avoid removing user data.
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(seed, unseed),
    ]
