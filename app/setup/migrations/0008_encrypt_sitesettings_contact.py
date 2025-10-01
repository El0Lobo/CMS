from django.db import migrations

import app.core.encryption


FIELDS_TO_ENCRYPT = [
    "org_name",
    "address_street",
    "address_number",
    "address_postal_code",
    "address_city",
    "address_country",
    "contact_email",
    "contact_phone",
    "same_as",
    "awareness_contact",
]


def encrypt_sitesettings(apps, schema_editor):
    SiteSettings = apps.get_model("setup", "SiteSettings")
    for settings in SiteSettings.objects.all():
        updated = False
        for field_name in FIELDS_TO_ENCRYPT:
            value = getattr(settings, field_name)
            if value in (None, ""):
                continue
            setattr(settings, field_name, value)
            updated = True
        if updated:
            settings.save(update_fields=FIELDS_TO_ENCRYPT + ["updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("setup", "0007_sitesettings_publish_opening_times"),
    ]

    operations = [
        migrations.AlterField(
            model_name="sitesettings",
            name="org_name",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address_street",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address_number",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address_postal_code",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=20),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address_city",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="address_country",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="contact_email",
            field=app.core.encryption.EncryptedEmailField(blank=True),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="contact_phone",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="same_as",
            field=app.core.encryption.EncryptedTextField(
                blank=True,
                help_text="schema.org sameAs: one URL per line",
            ),
        ),
        migrations.AlterField(
            model_name="sitesettings",
            name="awareness_contact",
            field=app.core.encryption.EncryptedCharField(
                blank=True,
                help_text="Phone, email, URL, or a short instruction (free text).",
                max_length=200,
            ),
        ),
        migrations.RunPython(encrypt_sitesettings, migrations.RunPython.noop),
    ]
