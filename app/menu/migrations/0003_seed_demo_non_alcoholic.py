
from django.db import migrations

def seed_demo(apps, schema_editor):
    Category = apps.get_model('menu', 'Category')
    Item = apps.get_model('menu', 'Item')
    ItemVariant = apps.get_model('menu', 'ItemVariant')
    Unit = apps.get_model('menu', 'Unit')

    try:
        nonalc = Category.objects.get(slug='drinks.non-alcoholic')
    except Category.DoesNotExist:
        return

    item, created = Item.objects.get_or_create(slug='sparkling.water', defaults={
        'name': 'Sparkling Water',
        'category': nonalc,
        'description': 'Refreshing fizzy water.',
        'visible_public': True,
    })
    L = Unit.objects.get(code='L')
    if not item.variants.exists():
        ItemVariant.objects.create(item=item, label='0.33', quantity=0.33, unit=L, price=2.50)
        ItemVariant.objects.create(item=item, label='0.5', quantity=0.5, unit=L, price=3.50)

class Migration(migrations.Migration):
    dependencies = [('menu', '0002_seed_defaults')]
    operations = [migrations.RunPython(seed_demo, migrations.RunPython.noop)]
