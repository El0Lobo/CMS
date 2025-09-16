from django.db import migrations, models
import django.db.models.deletion
import django.core.validators

class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=16, unique=True)),
                ('display', models.CharField(max_length=32)),
                ('kind', models.CharField(choices=[('volume', 'Volume'), ('mass', 'Mass'), ('count', 'Count')], max_length=16)),
            ],
            options={'ordering': ['kind', 'code']},
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120)),
                ('slug', models.SlugField(blank=True, max_length=140, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid “slug” (letters, numbers, underscores, hyphens).', regex='^[a-zA-Z0-9_-]+$')])),
                ('kind', models.CharField(choices=[('drink', 'Drinks'), ('food', 'Food')], max_length=16)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='menu.category')),
            ],
            options={'ordering': ['parent__id', 'name']},
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=160)),
                ('slug', models.SlugField(blank=True, max_length=180, unique=True, validators=[django.core.validators.RegexValidator(message='Enter a valid “slug” (letters, numbers, underscores, hyphens).', regex='^[a-zA-Z0-9_-]+$')])),
                ('description', models.TextField(blank=True)),
                ('vegan', models.BooleanField(default=False)),
                ('vegetarian', models.BooleanField(default=False)),
                ('gluten_free', models.BooleanField(default=False)),
                ('sugar_free', models.BooleanField(default=False)),
                ('lactose_free', models.BooleanField(default=False)),
                ('nut_free', models.BooleanField(default=False)),
                ('halal', models.BooleanField(default=False)),
                ('kosher', models.BooleanField(default=False)),
                ('visible_public', models.BooleanField(default=True)),
                ('featured', models.BooleanField(default=False)),
                ('sold_out_until', models.DateTimeField(blank=True, null=True)),
                ('new_until', models.DateTimeField(blank=True, null=True)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='items', to='menu.category')),
            ],
            options={'ordering': ['name']},
        ),
        migrations.CreateModel(
            name='ItemVariant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(blank=True, help_text='Optional label (e.g. ‘Bottle’, ‘Glass’, ‘Large’)', max_length=64)),
                ('quantity', models.DecimalField(decimal_places=3, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0)])),
                ('abv', models.DecimalField(blank=True, decimal_places=2, help_text='Alcohol by volume (%) — drinks only', max_digits=5, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variants', to='menu.item')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='menu.unit')),
            ],
            options={'ordering': ['item__name', 'unit__kind', 'quantity', 'label']},
        ),
    ]
