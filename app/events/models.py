"""Event domain models."""

from datetime import datetime

from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class EventCategory(models.Model):
    """High level labels (e.g. live band, DJ night, flea market)."""

    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(
        max_length=16,
        blank=True,
        help_text="Optional hex color (without #) used for UI accents.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class Event(models.Model):
    """Represents a public- or internal-facing happening at the venue."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        SCHEDULED = "scheduled", "Scheduled"
        PUBLISHED = "published", "Published"
        ARCHIVED = "archived", "Archived"
        CANCELLED = "cancelled", "Cancelled"

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    status = models.CharField(
        max_length=12, choices=Status.choices, default=Status.DRAFT
    )
    hero_image = models.ImageField(
        upload_to="events/hero/", blank=True, null=True
    )
    teaser = models.CharField(
        max_length=280,
        blank=True,
        help_text="Short summary for cards, social previews, SEO descriptions.",
    )
    description_public = models.TextField(
        blank=True, help_text="Markdown or HTML rendered on the public site."
    )
    description_internal = models.TextField(
        blank=True,
        help_text="Staff-only notes (door team briefings, settlement notes, etc.)",
    )

    categories = models.ManyToManyField(
        EventCategory,
        blank=True,
        related_name="events",
        help_text="Pick all that apply (used for filtering and SEO markup).",
    )

    doors_at = models.DateTimeField(blank=True, null=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField(blank=True, null=True)
    curfew_at = models.DateTimeField(blank=True, null=True)

    ticket_url = models.URLField(blank=True)
    ticket_price_from = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    ticket_price_to = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, null=True
    )
    is_free = models.BooleanField(default=False)

    requires_shifts = models.BooleanField(
        default=False,
        help_text="If checked, event will appear in the shift planner.",
    )
    standard_shifts = models.ManyToManyField(
        "shifts.ShiftTemplate",
        blank=True,
        related_name="events",
        help_text="Select standard shifts (door, bar, etc.) to generate for this event.",
    )

    venue_name = models.CharField(max_length=200, blank=True)
    venue_address = models.CharField(max_length=255, blank=True)
    venue_postal_code = models.CharField(max_length=32, blank=True)
    venue_city = models.CharField(max_length=120, blank=True)
    venue_country = models.CharField(max_length=120, blank=True)
    seo_title = models.CharField(max_length=70, blank=True)
    seo_description = models.CharField(max_length=160, blank=True)

    visibility_key = models.CharField(
        max_length=120,
        blank=True,
        help_text="Visibility rule key (managed via the setup visibility cogs).",
    )

    featured = models.BooleanField(default=False)
    published_at = models.DateTimeField(blank=True, null=True)
    archived_at = models.DateTimeField(blank=True, null=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="events_created",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="events_updated",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-starts_at", "title"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        if self.status in {self.Status.CANCELLED, self.Status.ARCHIVED} and not self.archived_at:
            self.archived_at = timezone.now()
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        return reverse("events:detail", args=[self.slug])

    @property
    def doors_time(self) -> datetime | None:
        return self.doors_at or self.starts_at


class EventPerformer(models.Model):
    """Performer slot (imported from Band or ad-hoc)."""

    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="performers")
    band = models.ForeignKey(
        "bands.Band",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="event_slots",
    )
    display_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Shown publicly; defaults to the linked band's name.",
    )
    performer_type = models.CharField(
        max_length=16,
        blank=True,
        help_text="Optional override (DJ set, acoustic, support, etc.).",
    )
    slot_starts_at = models.DateTimeField(blank=True, null=True)
    slot_ends_at = models.DateTimeField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "slot_starts_at", "display_name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.display_name} @ {self.event.title}"

    def sync_display_name(self):
        if self.band and not self.display_name:
            self.display_name = self.band.name

    def save(self, *args, **kwargs):
        self.sync_display_name()
        super().save(*args, **kwargs)
