# app/menu/views.py
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CategoryForm, ItemForm, ItemVariantFormSet
from .models import Category, Item

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Item   
# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _roots() -> tuple[Category | None, Category | None]:
    """
    Return the single root 'Drinks' and 'Food' categories, if present.
    We rely on seed data/migrations to have created them.
    """
    drinks = (
        Category.objects
        .filter(parent__isnull=True, kind=Category.KIND_DRINK)
        .first()
    )
    food = (
        Category.objects
        .filter(parent__isnull=True, kind=Category.KIND_FOOD)
        .first()
    )
    return drinks, food


def _now():
    """Convenience to keep templates consistent when showing 'now'."""
    return timezone.now()


# ---------------------------------------------------------------------------
# CMS: Dashboard & Lists
# ---------------------------------------------------------------------------

@login_required
def manage_menu(request):
    """
    Top-level CMS page for managing the menu tree.
    Warn if the expected roots are missing so the user knows to run seeds.
    """
    drinks_root, food_root = _roots()
    if not drinks_root or not food_root:
        messages.warning(
            request,
            "Drinks and Food root categories are missing. "
            "Run migrations/seed to create them."
        )
    return render(
        request,
        "menu/manage.html",
        {"drinks_root": drinks_root, "food_root": food_root, "now": _now()},
    )


@login_required
def items_list(request):
    """
    Flat list of all items (useful for quick edits/search).
    """
    items = (
        Item.objects
        .select_related("category")
        .prefetch_related("variants")
        .order_by("category__name", "name")
    )
    return render(request, "menu/items_list.html", {"items": items, "now": _now()})


# ---------------------------------------------------------------------------
# Categories (create/edit/delete)
# ---------------------------------------------------------------------------

@login_required
def category_create(request, root=None, parent_slug=None):
    """
    Create a category either under a specific parent or directly under a root
    ('drinks'/'food') by setting the form's allowed kind.
    """
    parent = None
    root_kind = None

    if parent_slug:
        parent = get_object_or_404(Category, slug=parent_slug)
        root_kind = parent.kind
    elif root in ("drinks", "food"):
        root_kind = Category.KIND_DRINK if root == "drinks" else Category.KIND_FOOD

    if request.method == "POST":
        form = CategoryForm(request.POST, root_kind=root_kind)
        if form.is_valid():
            obj = form.save()
            messages.success(request, f"Category “{obj.name}” created.")
            return redirect("menu:manage")
    else:
        form = CategoryForm(root_kind=root_kind, initial={"parent": parent})

    ctx = {"form": form, "parent": parent, "root_kind": root_kind}
    return render(request, "menu/category_form.html", ctx)


@login_required
def category_edit(request, slug):
    """
    Edit an existing category. The form constrains the 'kind' to match.
    """
    obj = get_object_or_404(Category, slug=slug)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=obj, root_kind=obj.kind)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated.")
            return redirect("menu:manage")
    else:
        form = CategoryForm(instance=obj, root_kind=obj.kind)

    return render(request, "menu/category_form.html", {"form": form, "obj": obj})


@login_required
def category_delete(request, slug):
    """
    Delete a non-root category. Root categories are protected.
    """
    obj = get_object_or_404(Category, slug=slug)

    if obj.parent is None:
        messages.error(request, "Cannot delete root categories.")
        return redirect("menu:manage")

    if request.method == "POST":
        obj.delete()
        messages.success(request, "Category deleted.")
        return redirect("menu:manage")

    return render(request, "menu/category_delete_confirm.html", {"obj": obj})


# ---------------------------------------------------------------------------
# Items (create/edit)
# ---------------------------------------------------------------------------

@login_required
@transaction.atomic
def item_create(request, parent_slug):
    """
    Create an item under the given parent category and manage its variants
    via an inline formset. The formset receives the parent kind so it can
    validate units/fields appropriately (drinks vs food).
    """
    parent = get_object_or_404(Category, slug=parent_slug)
    item = Item(category=parent)  # unsaved, used to bind the formset instance

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        formset = ItemVariantFormSet(
            request.POST,
            instance=item,
            form_kwargs={"item_kind": parent.kind},
        )

        if form.is_valid() and formset.is_valid():
            try:
                # Save parent first so it has a PK for formset relations.
                saved_item = form.save(commit=False)
                saved_item.category = parent
                saved_item.save()

                # Ensure formset is bound to the saved parent, then save.
                formset.instance = saved_item
                formset.save()

                messages.success(
                    request,
                    f"Item “{saved_item.name}” created in {parent.name}."
                )
                return redirect("menu:manage")

            except IntegrityError:
                messages.error(
                    request,
                    "Could not save item due to a database integrity error."
                )
                # fall through to render errors
    else:
        form = ItemForm(instance=item)
        formset = ItemVariantFormSet(
            instance=item,
            form_kwargs={"item_kind": parent.kind},
        )

    ctx = {
        "form": form,
        "formset": formset,
        "parent": parent,
        # no 'item' passed here to keep the template title “New item…”
    }
    return render(request, "menu/item_form.html", ctx)


@login_required
@transaction.atomic
def item_edit(request, slug):
    """
    Edit an item and its variants. We save the parent form first, then the
    variants formset, inside a transaction to keep things consistent.
    """
    item = get_object_or_404(Item, slug=slug)
    parent = item.category

    if request.method == "POST":
        form = ItemForm(request.POST, instance=item)
        formset = ItemVariantFormSet(
            request.POST,
            instance=item,
            form_kwargs={"item_kind": parent.kind},
        )

        if form.is_valid() and formset.is_valid():
            try:
                saved_item = form.save()  # already has category
                formset.instance = saved_item  # explicit, keeps things clear
                formset.save()

                messages.success(request, "Item updated.")
                return redirect("menu:manage")

            except IntegrityError:
                messages.error(
                    request,
                    "Could not update item due to a database integrity error."
                )
                # fall through to render errors
    else:
        form = ItemForm(instance=item)
        formset = ItemVariantFormSet(
            instance=item,
            form_kwargs={"item_kind": parent.kind},
        )

    ctx = {
        "form": form,
        "formset": formset,
        "parent": parent,
        "item": item,  # lets template show “Edit item …”
    }
    return render(request, "menu/item_form.html", ctx)

@login_required
@permission_required("menu.delete_item", raise_exception=True)
def item_delete(request, slug):
    item = get_object_or_404(Item, slug=slug)

    if request.method == "POST":
        name = item.name
        item.delete()
        messages.success(request, f'Item “{name}” was deleted.')
        return redirect("/cms/menu/") 
    return render(request, "menu/item_confirm_delete.html", {"item": item})