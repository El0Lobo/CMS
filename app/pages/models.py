from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

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
    slug = models.SlugField(max_length=200)
    summary = models.TextField(blank=True)
    body = CKEditor5Field("Body", blank=True, config_name="default")
    blocks = models.JSONField(
        default=list,
        blank=True,
        help_text="Structured block data used by the visual page builder.",
    )
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.DRAFT)
    is_visible = models.BooleanField(
        default=True,
        help_text="If disabled page stays in drafts and is hidden from navigation.",
    )
    navigation_order = models.PositiveIntegerField(default=0)
    show_navigation_bar = models.BooleanField(
        default=True,
        help_text="Display navigation bar on this page.",
    )
    custom_nav_items = models.JSONField(
        default=list,
        blank=True,
        help_text="Ordered list of page slugs to display when this page renders (leave empty to hide the navigation bar).",
    )
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
    render_body_only = models.BooleanField(
        default=False,
        help_text="If enabled, ignore block builder and render raw HTML body only.",
    )

    objects = PageQuerySet.as_manager()

    class Meta:
        ordering = ("navigation_order", "title")

    def __str__(self) -> str:
        return self.title

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

    def publish(self):
        self.status = Page.Status.PUBLISHED
        if not self.published_at:
            self.published_at = timezone.now()

    def render_content_segments(self, *, request=None, extra_context=None):
        """
        Render the page into main/footer fragments so templates can place them separately.
        """

        if self.render_body_only or not self.blocks:
            html = self.body or ""
            return mark_safe(html), mark_safe(""), mark_safe("")

        extra = dict(extra_context or {})
        extra.setdefault("nav_override", list(self.custom_nav_items or []))
        extra.setdefault("nav_show_bar", bool(self.show_navigation_bar))

        nav_blocks = [block for block in self.blocks if block.get("type") == "navigation"]
        footer_blocks = [block for block in self.blocks if block.get("type") == "footer"]
        main_blocks = [
            block
            for block in self.blocks
            if block.get("type") not in {"footer", "navigation"}
        ]

        main_html = render_blocks(main_blocks, request=request, extra_context=extra)
        footer_html = render_blocks(footer_blocks, request=request, extra_context=extra)
        if nav_blocks:
            nav_html = render_blocks(nav_blocks[:1], request=request, extra_context=extra)
        elif extra.get("nav_show_bar", True):
            default_props = {**DEFAULT_NAV_PROPS, "links": extra.get("nav_override") or []}
            nav_html = render_blocks(
                [{"type": "navigation", "props": default_props}],
                request=request,
                extra_context=extra,
            )
        else:
            nav_html = mark_safe("")
        return main_html, footer_html, nav_html

    def render_content(self, *, request=None, extra_context=None) -> str:
        """
        Render the page blocks to HTML. Falls back to legacy body if flagged or empty.
        """

        main_html, footer_html, nav_html = self.render_content_segments(
            request=request, extra_context=extra_context
        )
        return mark_safe(f"{nav_html}{main_html}{footer_html}")
DEFAULT_NAV_PROPS = {
    "show_logo": True,
    "logo_text": "",
    "show_language_switcher": True,
    "layout": "center",
    "links": [],
}
