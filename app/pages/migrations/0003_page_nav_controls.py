from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0002_page_blocks"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="custom_nav_items",
            field=models.JSONField(
                blank=True,
                default=list,
                help_text="Ordered list of page slugs to display when this page renders (leave empty to use the global navigation).",
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="show_navigation_bar",
            field=models.BooleanField(
                default=True,
                help_text="Display the navigation bar on this page.",
            ),
        ),
    ]
