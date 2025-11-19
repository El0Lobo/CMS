from django.db import migrations
import model_utils.fields
import recurrence.fields


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0007_event_recurrence_overrides_and_holidays"),
    ]

    operations = [
        migrations.AddField(
            model_name="event",
            name="recurrence_rule",
            field=recurrence.fields.RecurrenceField(
                blank=True,
                null=True,
                help_text="Advanced recurrence (RRULE/EXDATE). Leave empty to use the basic repeat options.",
            ),
        ),
        migrations.AlterField(
            model_name="event",
            name="created_at",
            field=model_utils.fields.AutoCreatedField(
                default=None, editable=False, verbose_name="created at"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="event",
            name="updated_at",
            field=model_utils.fields.AutoLastModifiedField(
                default=None, editable=False, verbose_name="updated at"
            ),
            preserve_default=False,
        ),
    ]
