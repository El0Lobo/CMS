from django.db import migrations

def add_demo(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    Item = apps.get_model('menu', 'Item')
    ItemVariant = apps.get_model('menu', 'ItemVariant')
    Unit = apps.get_model('menu', 'Unit')
    try:
        parent = Category.objects.get(slug="non-alcoholic")
        item, _ = Item.objects.get_or_create(slug="sparkling-water", defaults={
            "name": "Sparkling Water",
            "category": parent,
            "description": "Refreshing carbonated water.",
            "visible_public": True,
        })
        L = Unit.objects.get(code="L")
        # two sizes
        ItemVariant.objects.get_or_create(item=item, quantity=0.33, unit=L, defaults={"price": 2.50, "label": "Small"})
        ItemVariant.objects.get_or_create(item=item, quantity=0.5, unit=L, defaults={"price": 3.50, "label": "Large"})
    except Category.DoesNotExist:
        pass

def noop(apps, schema_editor):
    pass

class Migration(migrations.Migration):
    dependencies = [('menu', '0002_seed')]
    operations = [migrations.RunPython(add_demo, noop)]
