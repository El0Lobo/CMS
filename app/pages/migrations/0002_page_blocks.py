from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="blocks",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Structured block data used by the visual page builder.",
            ),
        ),
    ]
