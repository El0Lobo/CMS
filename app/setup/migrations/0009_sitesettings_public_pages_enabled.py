from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("setup", "0008_encrypt_sitesettings_contact"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="public_pages_enabled",
            field=models.BooleanField(
                default=True,
                help_text="Expose the public-facing site powered by the Pages app.",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="required_pages",
            field=models.TextField(
                blank=True,
                help_text="Legacy field for auto-created pages; no longer used by the UI.",
            ),
        ),
    ]
