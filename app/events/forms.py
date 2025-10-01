"""Forms for event management."""

from __future__ import annotations

from datetime import datetime, timedelta

from django import forms
from django.forms import BaseInlineFormSet, inlineformset_factory
from django.utils import timezone
from django.utils.text import slugify

from app.bands.models import Band
from app.events.models import Event, EventPerformer
from app.setup.models import SiteSettings
from app.shifts.models import ShiftTemplate


class EventForm(forms.ModelForm):
    """Main event form used for create/edit modals."""

    class Meta:
        model = Event
        fields = [
            "title",
            "slug",
            "status",
            "hero_image",
            "teaser",
            "description_public",
            "description_internal",
            "categories",
            "doors_at",
            "starts_at",
            "ends_at",
            "curfew_at",
            "ticket_url",
            "ticket_price_from",
            "ticket_price_to",
            "is_free",
            "requires_shifts",
            "standard_shifts",
            "venue_name",
            "venue_address",
            "venue_postal_code",
            "venue_city",
            "venue_country",
            "seo_title",
            "seo_description",
            "visibility_key",
            "featured",
        ]
        widgets = {
            "description_public": forms.Textarea(attrs={"rows": 6}),
            "description_internal": forms.Textarea(attrs={"rows": 4}),
            "doors_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "starts_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "ends_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "curfew_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "standard_shifts": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        tz = timezone.get_current_timezone()

        def to_naive(value):
            if not value:
                return value
            if timezone.is_naive(value):
                return value.replace(second=0, microsecond=0)
            return timezone.localtime(value).replace(second=0, microsecond=0, tzinfo=None)

        if "standard_shifts" in self.fields:
            queryset = ShiftTemplate.objects.order_by("order", "name")
            self.fields["standard_shifts"].queryset = queryset
        else:
            queryset = ShiftTemplate.objects.none()
        # Provide friendly defaults the first time an event is created.
        if not self.instance.pk:
            now = timezone.localtime()

            try:
                cfg = SiteSettings.get_solo()
            except Exception:  # pragma: no cover - in migrations / early boot
                cfg = None

            default_starts = now.replace(minute=0, second=0, microsecond=0) + timedelta(days=7)
            default_doors = default_starts - timedelta(hours=1)
            default_ends = default_starts + timedelta(hours=3)
            default_curfew = default_ends

            if cfg:
                self.initial.setdefault("venue_name", cfg.org_name)
                address_parts = [cfg.address_street, cfg.address_number]
                address_joined = " ".join(part for part in address_parts if part)
                self.initial.setdefault("venue_address", address_joined.strip())
                self.initial.setdefault("venue_postal_code", cfg.address_postal_code)
                self.initial.setdefault("venue_city", cfg.address_city)
                self.initial.setdefault("venue_country", cfg.address_country or "")

                openings = (
                    cfg.hours.filter(closed=False, open_time__isnull=False, close_time__isnull=False)
                    .order_by("weekday")
                )
                if openings:
                    def order_key(hour):
                        return ((hour.weekday - now.weekday()) % 7, hour.open_time)

                    first_slot = sorted(openings, key=order_key)[0]
                    days_until = (first_slot.weekday - now.weekday()) % 7
                    target_date = now.date() + timedelta(days=days_until)
                    doors_dt = timezone.make_aware(
                        datetime.combine(target_date, first_slot.open_time), tz
                    )
                    close_dt = timezone.make_aware(
                        datetime.combine(target_date, first_slot.close_time), tz
                    )
                    start_dt = doors_dt + timedelta(minutes=60)
                    if start_dt > close_dt:
                        start_dt = doors_dt

                    default_doors = doors_dt
                    default_starts = start_dt
                    default_ends = close_dt
                    default_curfew = close_dt

            self.initial.setdefault("doors_at", to_naive(default_doors))
            self.initial.setdefault("starts_at", to_naive(default_starts))
            self.initial.setdefault("ends_at", to_naive(default_ends))
            self.initial.setdefault("curfew_at", to_naive(default_curfew))

        # Provide nicer help-text for empty slug
        self.fields["slug"].help_text = (
            "Leave blank to auto-generate from the title."
        )
        self.fields["categories"].widget.attrs.update({"data-allow-search": "true"})
        if "standard_shifts" in self.fields:
            widget = self.fields["standard_shifts"].widget or forms.CheckboxSelectMultiple()
            if not isinstance(widget, forms.CheckboxSelectMultiple):
                widget = forms.CheckboxSelectMultiple()
            widget.choices = self.fields["standard_shifts"].choices
            self.fields["standard_shifts"].widget = widget
            self.fields["standard_shifts"].required = False
            if not self.instance.pk and queryset.exists():
                self.initial.setdefault("standard_shifts", list(queryset.values_list("id", flat=True)))
                self.initial.setdefault("requires_shifts", True)
                self.fields["requires_shifts"].initial = True

        for key in ["doors_at", "starts_at", "ends_at", "curfew_at"]:
            value = self.initial.get(key)
            if hasattr(value, "tzinfo") and value is not None:
                self.initial[key] = value.replace(tzinfo=None)

        self.fieldsets = [
            (
                "Basics",
                [
                    "title",
                    "status",
                    "slug",
                    "categories",
                    "featured",
                    "hero_image",
                    "teaser",
                ],
                {"open": True},
            ),
            (
                "Schedule",
                ["doors_at", "starts_at", "ends_at", "curfew_at"],
                {"open": True},
            ),
            (
                "Location",
                [
                    "venue_name",
                    "venue_address",
                    "venue_postal_code",
                    "venue_city",
                    "venue_country",
                ],
                {},
            ),
            (
                "Ticketing",
                [
                    "is_free",
                    "ticket_price_from",
                    "ticket_price_to",
                    "ticket_url",
                ],
                {},
            ),
            (
                "Content",
                [
                    "description_public",
                    "description_internal",
                    "seo_title",
                    "seo_description",
                ],
                {},
            ),
            (
                "Visibility",
                ["visibility_key"],
                {},
            ),
            (
                "Shifts",
                ["requires_shifts", "standard_shifts"],
                {},
            ),
        ]

        self.render_fieldsets = []
        for title, field_names, opts in self.fieldsets:
            bound_fields = [self[field] for field in field_names]
            self.render_fieldsets.append((title, bound_fields, opts))

        if "standard_shifts" in self.fields:
            self.standard_shift_count = self.fields["standard_shifts"].queryset.count()
        else:
            self.standard_shift_count = 0

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        if slug:
            qs = Event.objects.exclude(pk=self.instance.pk)
            if qs.filter(slug=slug).exists():
                raise forms.ValidationError("Slug already in use.")
        return slug

    def save(self, commit: bool = True):
        inst = super().save(commit=False)
        if self.user and not inst.pk:
            inst.created_by = self.user
        if self.user:
            inst.updated_by = self.user
        if commit:
            inst.save()
            self.save_m2m()
        else:
            # ensure categories saved when commit=False and saved later
            self._pending_m2m = self.cleaned_data.get("categories")
        return inst


class EventPerformerForm(forms.ModelForm):
    """Handles both linking an existing band and quick-adding one."""

    new_band_name = forms.CharField(
        required=False,
        label="Quick add band",
        help_text="Fill to create a new band on the fly if it does not exist.",
    )
    performer_type_override = forms.ChoiceField(
        required=False,
        choices=[("", "—")] + list(Band.PerformerType.choices),
        label="Performer type",
        help_text="Optional override if different from the band profile.",
    )

    class Meta:
        model = EventPerformer
        fields = [
            "band",
            "new_band_name",
            "display_name",
            "performer_type_override",
            "slot_starts_at",
            "slot_ends_at",
            "order",
            "notes",
        ]
        widgets = {
            "slot_starts_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "slot_ends_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 2}),
        }

    def clean(self):
        cleaned = super().clean()
        band = cleaned.get("band")
        quick_name = cleaned.get("new_band_name", "").strip()
        if self.cleaned_data.get("DELETE"):
            return cleaned
        if self.empty_permitted and not (band or quick_name or cleaned.get("display_name")):
            return cleaned
        if not band and not quick_name:
            raise forms.ValidationError("Select a band or quick-add one.")
        return cleaned

    def save(self, commit: bool = True):
        band = self.cleaned_data.get("band")
        quick_name = (self.cleaned_data.get("new_band_name") or "").strip()
        performer_type = self.cleaned_data.get("performer_type_override") or ""

        if not band and quick_name:
            defaults = {
                "slug": slugify(quick_name)[:220],
                "performer_type": performer_type or Band.PerformerType.BAND,
            }
            band, _ = Band.objects.get_or_create(name=quick_name, defaults=defaults)
        instance: EventPerformer = super().save(commit=False)
        instance.band = band
        if performer_type:
            instance.performer_type = performer_type
        elif band and not instance.performer_type:
            instance.performer_type = band.performer_type
        if not instance.display_name and band:
            instance.display_name = band.name
        if commit:
            instance.save()
        return instance


class BasePerformerFormSet(BaseInlineFormSet):
    def clean(self):
        super().clean()
        totals = 0
        for form in self.forms:
            if not getattr(form, "cleaned_data", None) or form.cleaned_data.get("DELETE"):
                continue
            data = form.cleaned_data
            has_content = data.get("band") or data.get("new_band_name") or data.get("display_name")
            if has_content:
                totals += 1
        if totals == 0:
            status = getattr(self.instance, "status", Event.Status.DRAFT)
            if status == Event.Status.PUBLISHED:
                raise forms.ValidationError("Published events must list at least one performer.")


EventPerformerFormSet = inlineformset_factory(
    Event,
    EventPerformer,
    form=EventPerformerForm,
    formset=BasePerformerFormSet,
    extra=1,
    can_delete=True,
)
