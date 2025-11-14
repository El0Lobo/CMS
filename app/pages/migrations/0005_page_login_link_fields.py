from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0004_remove_page_show_in_navigation"),
    ]

    operations = [
        migrations.AddField(
            model_name="page",
            name="login_link_label",
            field=models.CharField(
                blank=True,
                default="CMS Login",
                help_text="Text used for the login link when shown.",
                max_length=80,
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="login_link_url",
            field=models.CharField(
                blank=True,
                default="/accounts/login/",
                help_text="URL used for the login link (absolute or relative).",
                max_length=255,
            ),
        ),
        migrations.AddField(
            model_name="page",
            name="show_login_link",
            field=models.BooleanField(
                default=True,
                help_text="Show the login link when the navigation bar is visible.",
            ),
        ),
    ]
