# app/setup/forms.py
# ---------------------------------------------------------------------------
# Forms for the BAR CMS "setup" section (global site settings, hours, tiers,
# visibility rules). Everything is optional to allow partial saves.
# ---------------------------------------------------------------------------

from __future__ import annotations

from django import forms
from django.conf import settings as dj_settings
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django.forms.models import inlineformset_factory, modelformset_factory
from django.utils.text import slugify

from .models import SiteSettings, MembershipTier, OpeningHour, VisibilityRule


SMOKING_CHOICES = (
    ("", "— not specified —"),
    ("true", "Allowed"),
    ("false", "Not allowed"),
)


def guess_default_currency() -> str:
    tz = (getattr(dj_settings, "TIME_ZONE", "") or "").lower()
    if "london" in tz:
        return "GBP"
    if any(x in tz for x in ["zurich", "berlin", "paris", "madrid", "rome", "amsterdam", "vienna"]):
        return "EUR"
    if any(x in tz for x in ["new_york", "los_angeles", "chicago"]):
        return "USD"
    return "EUR"


def _update_widget(field: forms.Field, **attrs) -> None:
    field.widget.attrs.update(attrs)


class SettingsForm(ModelForm):
    """
    Primary form for global site settings.

    'required_pages' is persisted as newline-separated *pairs* in order:
        slug|label
    We prefer POST arrays `required_pages_slug[]` and `required_pages_label[]`
    (submitted by setup.html) so changing the label won't change the URL.

    Backward compatible:
      - If only `required_pages` is posted:
          • parse "slug|label" when present
          • otherwise treat the value as a label and derive slug via slugify
    """

    currency_text = forms.CharField(
        required=False,
        help_text="Pick from list or type your own.",
        widget=forms.TextInput(
            attrs={"list": "currency_list", "placeholder": "EUR", "id": "currency_text"}
        ),
    )

    # Policies & accessibility (unchanged)
    smoking_allowed = forms.TypedChoiceField(
        required=False,
        choices=SMOKING_CHOICES,
        widget=forms.Select,
        coerce=lambda v: {"true": True, "false": False}.get(v, None),
        label="Smoking allowed?",
        help_text="If left unspecified, no smoking policy is published.",
    )
    pets_allowed_text = forms.CharField(required=False, label="Pets")
    typical_age_range = forms.CharField(required=False, label="Typical age range")
    minors_policy_note = forms.CharField(required=False, label="Kids/Minors note")

    acc_step_free = forms.BooleanField(required=False, label="Step-free entrance")
    acc_wheelchair = forms.BooleanField(required=False, label="Wheelchair accessible")
    acc_accessible_wc = forms.BooleanField(required=False, label="Accessible restroom")
    acc_visual_aid = forms.BooleanField(required=False, label="Visual assistance available")
    acc_service_animals = forms.BooleanField(required=False, label="Service animals welcome")
    lgbtq_friendly = forms.BooleanField(required=False, label="LGBTQIA+ friendly")

    accessibility_summary = forms.CharField(required=False, widget=forms.Textarea)
    maximum_attendee_capacity = forms.IntegerField(required=False, min_value=0)
    awareness_team_available = forms.BooleanField(required=False)
    awareness_contact = forms.CharField(required=False, label="Awareness contact (free text)")

    class Meta:
        model = SiteSettings
        fields = [
            # General
            "mode", "org_name", "logo", "publish_opening_times",
            # Address & geodata
            "address_street", "address_number", "address_postal_code", "address_city",
            "address_country", "address_autocomplete",
            "geo_lat", "geo_lng", "price_range", "default_currency",
            # Contact & web
            "contact_email", "contact_phone", "website_url",
            # Socials
            "social_facebook", "social_instagram", "social_twitter", "social_tiktok",
            "social_youtube", "social_spotify", "social_soundcloud", "social_bandcamp",
            "social_linkedin", "social_mastodon",
            # SameAs
            "same_as",
            # Membership
            "membership_enabled", "membership_hint",
            # Public pages (stored as newline-separated slug|label pairs)
            "required_pages",
            # Policies & accessibility
            "smoking_allowed", "pets_allowed_text", "typical_age_range", "minors_policy_note",
            "acc_step_free", "acc_wheelchair", "acc_accessible_wc",
            "acc_visual_aid", "acc_service_animals", "lgbtq_friendly",
            "accessibility_summary", "maximum_attendee_capacity",
            "awareness_team_available", "awareness_contact",
        ]
        widgets = {
            "same_as": forms.Textarea(attrs={"rows": 3, "placeholder": "https://example.com\nhttps://twitter.com/your-handle"}),
            "price_range": forms.TextInput(attrs={"placeholder": "$$, $$$"}),
            "contact_email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "website_url": forms.URLInput(attrs={"placeholder": "https://example.com"}),
            "social_facebook":   forms.URLInput(attrs={"placeholder": "https://facebook.com/yourpage"}),
            "social_instagram":  forms.URLInput(attrs={"placeholder": "https://instagram.com/yourhandle"}),
            "social_twitter":    forms.URLInput(attrs={"placeholder": "https://x.com/yourhandle"}),
            "social_tiktok":     forms.URLInput(attrs={"placeholder": "https://tiktok.com/@yourhandle"}),
            "social_youtube":    forms.URLInput(attrs={"placeholder": "https://youtube.com/@yourchannel"}),
            "social_spotify":    forms.URLInput(attrs={"placeholder": "https://open.spotify.com/artist/..."}),
            "social_soundcloud": forms.URLInput(attrs={"placeholder": "https://soundcloud.com/yourhandle"}),
            "social_bandcamp":   forms.URLInput(attrs={"placeholder": "https://yourname.bandcamp.com"}),
            "social_linkedin":   forms.URLInput(attrs={"placeholder": "https://linkedin.com/company/your-company"}),
            "social_mastodon":   forms.URLInput(attrs={"placeholder": "https://mastodon.social/@yourhandle"}),
        }
        labels = {
            "address_street": "Street address",
            "address_number": "Street number",
            "address_postal_code": "ZIP or postal code (optional)",
            "address_city": "City",
            "address_country": "Country or region",
            "contact_email": "Email",
            "contact_phone": "Phone",
            "website_url": "Website",
            "same_as": "Same as",
            "price_range": "Price range",
            "default_currency": "Default currency",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["currency_text"].initial = (
            self.instance.default_currency or guess_default_currency()
        )

        if not self.instance.mode:
            self.initial.setdefault("mode", "venue")

        self.use_required_attribute = False
        for f in self.fields.values():
            f.required = False
            f.error_messages["required"] = ""

        upd = lambda name, **attrs: _update_widget(self.fields[name], **attrs) if name in self.fields else None
        upd("address_street", id="street-address", autocomplete="address-line1", enterkeyhint="next")
        upd("address_number", id="street-number", autocomplete="address-line2", enterkeyhint="next")
        upd("address_postal_code", id="postal-code", autocomplete="postal-code", enterkeyhint="next", **{"class": "postal-code"})
        upd("address_city", id="city", autocomplete="address-level2", enterkeyhint="next")
        upd("address_country", id="country", autocomplete="country", enterkeyhint="done")

    def clean(self):
        data = super().clean()

        # ---- Currency
        cur_from_post = self.data.get("currency_text")
        cur_from_clean = self.cleaned_data.get("currency_text")
        cur_from_model_field = self.cleaned_data.get("default_currency")
        cur = (cur_from_post or cur_from_clean or cur_from_model_field or guess_default_currency() or "EUR").upper()
        data["default_currency"] = cur
        self.cleaned_data["default_currency"] = cur

        # ---- Public pages (ordered pairs)
        pairs = []

        slugs  = [s.strip() for s in self.data.getlist("required_pages_slug") if s.strip()]
        labels = [s.strip() for s in self.data.getlist("required_pages_label") if s.strip()]

        if slugs and labels and len(slugs) == len(labels):
            for s, lbl in zip(slugs, labels):
                s_norm = slugify(s) or slugify(lbl) or "page"
                pairs.append((s_norm, lbl))
        else:
            # Backward compatibility: `required_pages` may be:
            #  - "slug|label" lines
            #  - plain labels -> derive slug (URL will follow label in this legacy path)
            raw = [s for s in self.data.getlist("required_pages") if s]
            for item in raw:
                line = item.strip()
                if not line:
                    continue
                if "|" in line:
                    s, lbl = line.split("|", 1)
                    s_norm = slugify(s) or slugify(lbl) or "page"
                    pairs.append((s_norm, lbl.strip()))
                else:
                    lbl = line
                    s_norm = slugify(lbl) or "page"
                    pairs.append((s_norm, lbl))

        # De-dupe by slug while preserving first occurrence order
        seen = set()
        deduped = []
        for s, lbl in pairs:
            if s in seen:
                continue
            seen.add(s)
            deduped.append((s, lbl))

        if deduped:
            # Persist as newline-separated "slug|label" lines
            joined = "\n".join(f"{s}|{lbl}" for s, lbl in deduped)
            data["required_pages"] = joined
            self.cleaned_data["required_pages"] = joined

        return data


class OpeningHourForm(ModelForm):
    class Meta:
        model = OpeningHour
        fields = ["weekday", "closed", "open_time", "close_time"]
        widgets = {
            "weekday": forms.HiddenInput(),
            "open_time": forms.TimeInput(attrs={"type": "time"}),
            "close_time": forms.TimeInput(attrs={"type": "time"}),
        }

    def clean_weekday(self):
        return self.instance.weekday


TierFormSet = inlineformset_factory(
    parent_model=SiteSettings,
    model=MembershipTier,
    fields=["name", "months", "price_minor", "active"],
    extra=1,
    can_delete=True,
)

HourFormSet = inlineformset_factory(
    parent_model=SiteSettings,
    model=OpeningHour,
    form=OpeningHourForm,
    fields=["weekday", "closed", "open_time", "close_time"],
    extra=0,
    can_delete=False,
    max_num=7,
)

GroupFormSet = modelformset_factory(
    model=Group,
    fields=["name"],
    extra=1,
    can_delete=True,
)


class VisibilityRuleForm(ModelForm):
    class Meta:
        model = VisibilityRule
        fields = ["key", "label", "is_enabled", "allowed_groups", "notes"]
        widgets = {"allowed_groups": forms.CheckboxSelectMultiple}
