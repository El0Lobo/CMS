from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0009_normalise_nav_items"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="render_body_only",
            field=models.BooleanField(
                default=False,
                help_text="If enabled, ignore the block builder and render the raw HTML body only.",
            ),
        ),
    ]
