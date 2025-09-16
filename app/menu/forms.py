# app/menu/forms.py
from django import forms
from django.forms import inlineformset_factory
from .models import Category, Item, ItemVariant, Unit


class CategoryForm(forms.ModelForm):
    """
    Form for creating/editing menu categories.
    - Enforces that parent categories are from the same kind (drink/food).
    - Root kind is passed in via `root_kind` on initialization.
    """

    class Meta:
        model = Category
        fields = ["name", "parent"]
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Category name"
            }),
            "parent": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        self.root_kind = kwargs.pop("root_kind", None)  # passed from view
        super().__init__(*args, **kwargs)

        # Determine kind: existing instance or root passed in
        kind = self.instance.kind if self.instance and self.instance.pk else self.root_kind

        # Restrict parent selection to same kind
        qs = Category.objects.filter(kind=kind) if kind else Category.objects.all()
        self.fields["parent"].queryset = qs

    def save(self, commit=True):
        """
        Ensure `kind` is set based on parent or root_kind.
        """
        obj = super().save(commit=False)
        if obj.parent:
            obj.kind = obj.parent.kind
        elif self.root_kind:
            obj.kind = self.root_kind
        if commit:
            obj.save()
        return obj



class ItemForm(forms.ModelForm):
    visible_public = forms.BooleanField(required=False, label="Show on public menu")
    featured = forms.BooleanField(required=False, label="Feature this item")
    sold_out_until = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}))
    new_until = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={"type": "datetime-local", "class": "form-control"}))

    class Meta:
        model = Item
        fields = [
            "name", "description",
            "visible_public", "featured",
            "sold_out_until", "new_until",
            "vegan", "vegetarian", "gluten_free", "sugar_free",
            "lactose_free", "nut_free", "halal", "kosher",
        ]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Item name"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Optional description"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove ":" after all labels rendered via label_tag
        self.label_suffix = ""

class ItemVariantForm(forms.ModelForm):
    """
    Form for item variants (e.g., Small/0.5 L vs. Large/1.0 L).
    - Restricts available units depending on item kind (drinks vs. food).
    - Hides ABV field for food.
    """

    class Meta:
        model = ItemVariant
        fields = ["label", "quantity", "unit", "price", "abv"]
        widgets = {
            "label": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "e.g. Glass, Bottle, Large"
            }),
            "quantity": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01", "min": "0"
            }),
            "unit": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.01", "min": "0"
            }),
            "abv": forms.NumberInput(attrs={
                "class": "form-control",
                "step": "0.1", "min": "0", "max": "100"
            }),
        }

    def __init__(self, *args, **kwargs):
        self.item_kind = kwargs.pop("item_kind", None)  # passed from view
        super().__init__(*args, **kwargs)

        # Restrict units by kind
        if self.item_kind == Category.KIND_DRINK:
            self.fields["unit"].queryset = Unit.objects.filter(code__in=["L", "mL"]).order_by("code")
            self.fields["quantity"].widget.attrs.update({"min": "0.01"})
        else:
            self.fields["unit"].queryset = Unit.objects.filter(code__in=["g", "pcs"]).order_by("code")
            self.fields["abv"].widget = forms.HiddenInput()
            self.fields["abv"].required = False

    def clean(self):
        """
        Hook for variant-specific validations.
        (Currently no hard caps on quantity — only basic filtering per kind.)
        """
        cleaned = super().clean()
        return cleaned


# Inline formset for managing multiple variants inside the item form
ItemVariantFormSet = inlineformset_factory(
    Item, ItemVariant,
    form=ItemVariantForm,
    extra=2,
    can_delete=True
)
