import json

from django import forms
from django.utils.text import slugify

from .models import Page


class PageForm(forms.ModelForm):
    body = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
    )
    blocks = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"data-page-blocks": "json"}),
    )
    custom_nav_items = forms.CharField(
        required=False,
        widget=forms.HiddenInput(attrs={"data-nav-items": "json"}),
    )

    class Meta:
        model = Page
        fields = [
            "title",
            "slug",
            "summary",
            "status",
            "is_visible",
            "show_navigation_bar",
            "render_body_only",
            "navigation_order",
            "custom_nav_items",
            "hero_image",
            "body",
            "blocks",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
            "navigation_order": forms.NumberInput(attrs={"min": 0}),
            "render_body_only": forms.CheckboxInput(),
        }

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        title = self.cleaned_data.get("title")
        if slug:
            return slugify(slug)
        if title:
            return slugify(title)
        return slug

    def clean_blocks(self):
        data = self.cleaned_data.get("blocks")
        if not data:
            return []
        if isinstance(data, list):
            return data
        try:
            parsed = json.loads(data)
        except json.JSONDecodeError as exc:  # pragma: no cover - user input
            raise forms.ValidationError("Blocks payload must be valid JSON.") from exc
        if not isinstance(parsed, list):
            raise forms.ValidationError("Blocks payload must be a JSON array.")
        return parsed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        initial_nav = self.instance.custom_nav_items if self.instance and self.instance.custom_nav_items else []
        try:
            initial_json = json.dumps(initial_nav)
        except TypeError:
            initial_json = "[]"
        self.fields["custom_nav_items"].initial = initial_json
        self.initial["custom_nav_items"] = initial_json

    def clean_custom_nav_items(self):
        raw = self.cleaned_data.get("custom_nav_items") or "[]"
        if isinstance(raw, list):
            parsed = raw
        else:
            try:
                parsed = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise forms.ValidationError("Navigation items payload must be JSON.") from exc
        if not isinstance(parsed, list):
            raise forms.ValidationError("Navigation items must be an array.")
        cleaned = []
        for slug in parsed:
            if not isinstance(slug, str):
                continue
            slug_norm = slugify(slug.strip()) or slug.strip()
            if slug_norm == "__login":
                slug_norm = "login"
            if not slug_norm or slug_norm in cleaned:
                continue
            cleaned.append(slug_norm)
        return cleaned

    def clean(self):
        data = super().clean()
        if not data.get("show_navigation_bar"):
            data["custom_nav_items"] = []
            self.cleaned_data["custom_nav_items"] = []
        return data


class PagePreviewForm(PageForm):
    """
    Variant of PageForm that skips unique validation so we can preview drafts
    without colliding on existing slugs.
    """

    def validate_unique(self):
        # Skip unique checks for preview-only rendering.
        return
