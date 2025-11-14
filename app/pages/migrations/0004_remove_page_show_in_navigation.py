from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0003_page_nav_controls"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="page",
            name="show_in_navigation",
        ),
    ]
