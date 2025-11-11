from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from .blocks import render_blocks


class PageQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=Page.Status.PUBLISHED, published_at__isnull=False)

    def visible(self):
        return self.published().filter(is_visible=True)


class Page(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        REVIEW = "review", "Needs review"
        PUBLISHED = "published", "Published"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    summary = models.TextField(blank=True)
    body = RichTextUploadingField(blank=True)
    blocks = models.JSONField(
        default=list,
        blank=True,
        help_text="Structured block data used by the visual page builder.",
    )
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT)
    is_visible = models.BooleanField(
        default=True,
        help_text="If disabled the page stays in drafts and is hidden from navigation.",
    )
    show_in_navigation = models.BooleanField(
        default=True,
        help_text="Show in public navigation if the page is published and visible.",
    )
    navigation_order = models.PositiveIntegerField(default=0)
    hero_image = models.ImageField(upload_to="pages/heroes/", blank=True, null=True)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pages_created",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="pages_updated",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )

    objects = PageQuerySet.as_manager()

    class Meta:
        ordering = ("navigation_order", "title")

    def __str__(self) -> str:
        return self.title

    def publish(self):
        self.status = Page.Status.PUBLISHED
        if not self.published_at:
            self.published_at = timezone.now()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Normalise blocks to always be a list
        if isinstance(self.blocks, tuple):
            self.blocks = list(self.blocks)
        if self.blocks is None:
            self.blocks = []
        if self.status != Page.Status.PUBLISHED:
            self.published_at = None
        elif not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        from django.urls import reverse

        return reverse("public:page-detail", kwargs={"slug": self.slug})

    def render_content(self, *, request=None, extra_context=None) -> str:
        """
        Render the page blocks to HTML. Falls back to legacy body if no blocks are defined.
        """

        if self.blocks:
            return render_blocks(self.blocks, request=request, extra_context=extra_context)
        return self.body or ""
