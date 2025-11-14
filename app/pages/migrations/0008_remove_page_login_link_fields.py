from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0007_alter_page_login_link_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="page",
            name="login_link_label",
        ),
        migrations.RemoveField(
            model_name="page",
            name="login_link_url",
        ),
        migrations.RemoveField(
            model_name="page",
            name="show_login_link",
        ),
    ]
