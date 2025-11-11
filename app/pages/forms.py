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

    class Meta:
        model = Page
        fields = [
            "title",
            "slug",
            "summary",
            "status",
            "is_visible",
            "show_in_navigation",
            "navigation_order",
            "hero_image",
            "body",
            "blocks",
        ]
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
            "navigation_order": forms.NumberInput(attrs={"min": 0}),
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


class PagePreviewForm(PageForm):
    """
    Variant of PageForm that skips unique validation so we can preview drafts
    without colliding on existing slugs.
    """

    def validate_unique(self):
        # Skip unique checks for preview-only rendering.
        return
