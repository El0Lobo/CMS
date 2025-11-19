from django.db import migrations
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ("pages", "0010_page_render_body_only"),
    ]

    operations = [
        migrations.AlterField(
            model_name="page",
            name="created_at",
            field=model_utils.fields.AutoCreatedField(
                default=None, editable=False, verbose_name="created at"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="page",
            name="updated_at",
            field=model_utils.fields.AutoLastModifiedField(
                default=None, editable=False, verbose_name="updated at"
            ),
            preserve_default=False,
        ),
    ]
