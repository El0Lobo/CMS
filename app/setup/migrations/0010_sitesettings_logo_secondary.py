from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("setup", "0009_sitesettings_public_pages_enabled"),
    ]

    operations = [
        migrations.AddField(
            model_name="sitesettings",
            name="logo_secondary",
            field=models.ImageField(blank=True, null=True, upload_to="logos/"),
        ),
    ]
