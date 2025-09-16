from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.db import models

class SiteSettings(models.Model):
    class Mode(models.TextChoices):
        VENUE = "VENUE", _("Venue / Club")
        BAND = "BAND", _("Band / Artist")
        PERSON = "PERSON", _("Person / Blog")

    # General
    mode = models.CharField(max_length=10, choices=Mode.choices, default=Mode.VENUE)
    org_name = models.CharField(max_length=200, blank=True)
    logo = models.ImageField(upload_to="logos/", blank=True, null=True)

    # Address (structured)
    address_street = models.CharField(max_length=200, blank=True)
    address_number = models.CharField(max_length=20, blank=True)
    address_postal_code = models.CharField(max_length=20, blank=True)
    address_city = models.CharField(max_length=120, blank=True)
    address_country = models.CharField(max_length=120, blank=True)
    address_autocomplete = models.BooleanField(
        default=False,
        help_text=_("Enable address autocomplete (requires JS integration)."),
    )

    # Contact / Socials
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=64, blank=True)
    website_url = models.URLField(blank=True)
    social_facebook = models.URLField(blank=True)
    social_instagram = models.URLField(blank=True)
    social_twitter = models.URLField(blank=True, help_text=_("X / Twitter URL"))
    social_tiktok = models.URLField(blank=True)
    social_youtube = models.URLField(blank=True)
    social_spotify = models.URLField(blank=True)
    social_soundcloud = models.URLField(blank=True)
    social_bandcamp = models.URLField(blank=True)
    social_linkedin = models.URLField(blank=True)
    social_mastodon = models.URLField(blank=True)
    same_as = models.TextField(blank=True, help_text=_("schema.org sameAs: one URL per line"))

    # schema.org-ish extras
    geo_lat = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, help_text=_("Latitude")
    )
    geo_lng = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True, help_text=_("Longitude")
    )
    price_range = models.CharField(max_length=20, blank=True, help_text=_("e.g., $, $$, $$$"))
    default_currency = models.CharField(
        max_length=8, default="EUR", help_text=_("Currency code (suggested list + free text)")
    )

    # Membership config
    membership_enabled = models.BooleanField(default=False)
    membership_hint = models.CharField(
        max_length=200, blank=True, help_text=_("Short label shown next to money icon.")
    )

    # Pages (for auto-create)
    required_pages = models.TextField(
        blank=True, help_text=_("One page title per line (created if app.pages.Page exists).")
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # --- Policies & accessibility ------------------------------------------------

    # Smoking policy (tri-state)
    smoking_allowed = models.BooleanField(null=True, blank=True)

    # Pets free text (“dogs only”, “no pets”, etc.)
    pets_allowed_text = models.CharField(max_length=120, blank=True)

    # Family friendliness (age range)
    typical_age_range = models.CharField(max_length=20, blank=True)

    # Accessibility toggles
    acc_step_free = models.BooleanField(default=False)
    acc_wheelchair = models.BooleanField(default=False)
    acc_accessible_wc = models.BooleanField(default=False)
    acc_visual_aid = models.BooleanField(default=False)
    acc_service_animals = models.BooleanField(default=False)

    accessibility_summary = models.TextField(blank=True)

    # LGBTQIA+ friendly badge/toggle
    lgbtq_friendly = models.BooleanField(default=False)

    # Short note for minors policy, e.g. “People under 16 only in company of an adult.”
    minors_policy_note = models.CharField(max_length=200, blank=True)

    # Capacity default for events
    maximum_attendee_capacity = models.PositiveIntegerField(null=True, blank=True)

    # Awareness team availability + single free-text contact
    awareness_team_available = models.BooleanField(default=False)
    awareness_contact = models.CharField(
        max_length=200,
        blank=True,
        help_text=_("Phone, email, URL, or a short instruction (free text)."),
    )
    publish_opening_times = models.BooleanField(
        default=False,
        verbose_name="Show opening times on public pages",
        help_text="If checked, opening times will be rendered on public pages."
    )
    def __str__(self):
        return f"Site Settings ({self.get_mode_display()})"

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(id=1)
        return obj


class MembershipTier(models.Model):
    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="tiers")
    name = models.CharField(max_length=120)
    months = models.PositiveIntegerField(default=12)
    price_minor = models.PositiveIntegerField(
        default=0, help_text=_("In minor units (e.g. cents/rappen)")
    )
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("settings", "name")

    def __str__(self):
        return f"{self.name} ({self.months} months)"


class OpeningHour(models.Model):
    settings = models.ForeignKey(SiteSettings, on_delete=models.CASCADE, related_name="hours")
    weekday = models.IntegerField(
        choices=[(i, d) for i, d in enumerate(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])],
        default=0,
    )
    closed = models.BooleanField(default=False)
    open_time = models.TimeField(null=True, blank=True)
    close_time = models.TimeField(null=True, blank=True)

    class Meta:
        unique_together = ("settings", "weekday")

    def __str__(self):
        if self.closed:
            return f"{self.get_weekday_display()}: closed"
        return f"{self.get_weekday_display()}: {self.open_time}–{self.close_time}"


class VisibilityRule(models.Model):
    """Attach visibility (allowed groups) to a component key used in templates."""
    key = models.CharField(
        max_length=120,
        unique=True,
            db_index=True,
            validators=[RegexValidator(
                r'^[\w\.\-:]+$',
                'Key may contain letters, numbers, underscores, hyphens, dots, or colons.'
            )],
    )
    label = models.CharField(max_length=200, blank=True, help_text=_("Human-friendly name; editable."))
    is_enabled = models.BooleanField(default=True)
    allowed_groups = models.ManyToManyField(Group, blank=True)
    notes = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.label or self.key
