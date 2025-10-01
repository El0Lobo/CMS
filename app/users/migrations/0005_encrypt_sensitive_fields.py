from django.db import migrations

import app.core.encryption


SENSITIVE_FIELDS = [
    "legal_name",
    "chosen_name",
    "pronouns",
    "birth_date",
    "email",
    "phone",
    "address",
    "role_title",
    "duties",
]


def encrypt_userprofile_fields(apps, schema_editor):
    UserProfile = apps.get_model("users", "UserProfile")
    for profile in UserProfile.objects.all():
        updated = False
        for field_name in SENSITIVE_FIELDS:
            value = getattr(profile, field_name)
            if value in (None, ""):
                continue
            setattr(profile, field_name, value)
            updated = True
        if updated:
            profile.save(update_fields=SENSITIVE_FIELDS + ["updated_at"])


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_fieldpolicy_options_alter_userprofile_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userprofile",
            name="legal_name",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="chosen_name",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="pronouns",
            field=app.core.encryption.EncryptedCharField(
                blank=True,
                help_text="e.g. she/her, he/him, they/them",
                max_length=64,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="birth_date",
            field=app.core.encryption.EncryptedDateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="email",
            field=app.core.encryption.EncryptedEmailField(blank=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="phone",
            field=app.core.encryption.EncryptedCharField(blank=True, max_length=64),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="address",
            field=app.core.encryption.EncryptedTextField(blank=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="role_title",
            field=app.core.encryption.EncryptedCharField(
                blank=True,
                help_text="Free-text role label, e.g. 'Bar lead'",
                max_length=120,
            ),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="duties",
            field=app.core.encryption.EncryptedTextField(blank=True),
        ),
        migrations.RunPython(encrypt_userprofile_fields, migrations.RunPython.noop),
    ]

