from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0006_alter_page_custom_nav_items"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="login_link_label",
            field=models.CharField(
                blank=True,
                default="Login",
                help_text="Text used for the login link when shown.",
                max_length=80,
            ),
        ),
        migrations.AlterField(
            model_name="page",
            name="login_link_url",
            field=models.CharField(
                blank=True,
                default="/login/",
                help_text="URL used for the login link (absolute or relative).",
                max_length=255,
            ),
        ),
    ]
