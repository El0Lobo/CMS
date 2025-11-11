from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=200)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("summary", models.TextField(blank=True)),
                ("body", ckeditor_uploader.fields.RichTextUploadingField(blank=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("draft", "Draft"),
                            ("review", "Needs review"),
                            ("published", "Published"),
                        ],
                        default="draft",
                        max_length=15,
                    ),
                ),
                (
                    "is_visible",
                    models.BooleanField(
                        default=True,
                        help_text="If disabled the page stays in drafts and is hidden from navigation.",
                    ),
                ),
                (
                    "show_in_navigation",
                    models.BooleanField(
                        default=True,
                        help_text="Show in public navigation if the page is published and visible.",
                    ),
                ),
                ("navigation_order", models.PositiveIntegerField(default=0)),
                (
                    "hero_image",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="pages/heroes/",
                    ),
                ),
                ("published_at", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pages_created",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "updated_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="pages_updated",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ("navigation_order", "title"),
            },
        ),
    ]
