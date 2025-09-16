# app/assets/views.py
import os
import mimetypes

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q, F, Case, When, CharField
from django.http import (
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseForbidden,
    Http404,
    FileResponse,
)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import AssetFilterForm, AssetCreateForm, CollectionForm, TagForm
from .models import Asset, Collection, Tag, VISIBILITY_MODE_CHOICES
from app.setup.helpers import is_allowed
from app.setup.models import VisibilityRule


# ---------- helpers -----------------------------------------------------------

def _base_queryset():
    return (
        Asset.objects.select_related("collection")
        .prefetch_related("tags", "collection__tags", "collection__allowed_groups")
        .annotate(
            eff_vis=Case(
                When(visibility="inherit", then=F("collection__visibility_mode")),
                default=F("visibility"),
                output_field=CharField(),
            )
        )
    )


def _query_assets(request):
    qs = _base_queryset()
    form = AssetFilterForm(request.GET or None)

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            qs = qs.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(slug__icontains=q)
                | Q(file__icontains=q)
                | Q(url__icontains=q)
                | Q(text_content__icontains=q)
                | Q(tags__name__icontains=q)
                | Q(collection__title__icontains=q)
                | Q(collection__slug__icontains=q)
                | Q(collection__tags__name__icontains=q)
            ).distinct()

        kind = form.cleaned_data.get("kind")
        if kind:
            qs = qs.filter(kind=kind)

        visibility = form.cleaned_data.get("visibility")
        if visibility in ("public", "internal", "groups"):
            qs = qs.filter(eff_vis=visibility)

        collection = form.cleaned_data.get("collection")
        if collection:
            qs = qs.filter(collection=collection)

        tags = form.cleaned_data.get("tags")
        if tags:
            qs = qs.filter(tags__in=list(tags)).distinct()

        source = form.cleaned_data.get("source")
        if source == "local":
            qs = qs.filter(file__isnull=False)
        elif source == "external":
            qs = qs.filter(file__isnull=True, url__isnull=False)

    return form, qs


def _user_group_ids(user):
    if not user.is_authenticated:
        return set()
    return set(user.groups.values_list("id", flat=True))


def _user_can_view_asset(user, asset: Asset) -> bool:
    """
    Public → everyone
    Internal → must be authenticated
    Groups → must be authenticated and in any allowed group for the collection
    """
    vis = getattr(asset, "effective_visibility", None) or getattr(asset, "eff_vis", None)
    if not vis:
        # fallback if property/annotation missing
        vis = asset.visibility
        if vis == "inherit" and asset.collection_id:
            vis = asset.collection.visibility_mode

    if vis == "public":
        return True
    if not user.is_authenticated:
        return False
    if vis == "internal":
        return True
    if vis == "groups":
        if not asset.collection_id:
            return False
        user_groups = _user_group_ids(user)
        allowed = set(asset.collection.allowed_groups.values_list("id", flat=True))
        return bool(user_groups & allowed)
    return False


def _allowed_for(user, key: str) -> bool:
    """Check if user is allowed for a given visibility key.
    Superusers pass; non-superusers require an explicit enabled rule AND membership per rule.
    """
    if user.is_superuser:
        return True
    try:
        return VisibilityRule.objects.filter(key=key, is_enabled=True).exists() and is_allowed(user, key)
    except Exception:
        return False


# ---------- index -------------------------------------------------------------

@login_required
def assets_index(request):
    # Page-level visibility (configurable via cog)
    if not is_allowed(request.user, "cms.assets.page"):
        return HttpResponseForbidden("You do not have access to this page.")
    create_form = None
    collection_form = None
    tag_form = None

    # Handle create actions (rule-based instead of staff)
    if request.method == "POST":
        action = (request.POST.get("action") or "create_asset").strip()

        if action == "create_collection":
            if not _allowed_for(request.user, "cms.assets.add_collection"):
                return HttpResponseForbidden("Not allowed")
            collection_form = CollectionForm(request.POST)
            if collection_form.is_valid():
                collection_form.save()
                return HttpResponseRedirect(reverse("assets:index"))

        elif action == "create_tag":
            if not _allowed_for(request.user, "cms.assets.add_tag"):
                return HttpResponseForbidden("Not allowed")
            tag_form = TagForm(request.POST)
            if tag_form.is_valid():
                tag_form.save()
                return HttpResponseRedirect(reverse("assets:index"))

        else:
            if not _allowed_for(request.user, "cms.assets.add_asset"):
                return HttpResponseForbidden("Not allowed")
            create_form = AssetCreateForm(request.POST, request.FILES)
            if create_form.is_valid():
                if not create_form.cleaned_data.get("appears_on"):
                    create_form.instance.appears_on = request.GET.get("appears_on") or ""
                create_form.save()
                return HttpResponseRedirect(reverse("assets:index"))

    # Listing + filtering
    filter_form, qs = _query_assets(request)

    # Apply visibility for all users (no staff bypass)
    user_groups = _user_group_ids(request.user)
    allowed_q = Q(eff_vis="public")
    if request.user.is_authenticated:
        allowed_q = allowed_q | Q(eff_vis="internal")
        if user_groups:
            allowed_q = allowed_q | Q(eff_vis="groups", collection__allowed_groups__id__in=list(user_groups))

    # Also include assets explicitly allowed by VisibilityRule keys (cog-based overrides)
    allowed_by_rule_ids = []
    for a in qs:
        try:
            akey = f"assets.asset.{a.id}"
            ckey = f"assets.collection.{a.collection_id}" if a.collection_id else None
            g_asset_actions = f"cms.assets.asset.{a.id}.actions"
            g_col_actions = f"cms.assets.collection.{a.collection_id}.actions" if a.collection_id else None
            g_col_toolbar = f"cms.assets.collection.{a.collection_id}.toolbar" if a.collection_id else None

            def rule_allows(key: str | None) -> bool:
                return bool(key) and VisibilityRule.objects.filter(key=key, is_enabled=True).exists() and is_allowed(request.user, key)

            if rule_allows(akey) or rule_allows(ckey) or rule_allows(g_asset_actions) or rule_allows(g_col_actions) or rule_allows(g_col_toolbar):
                allowed_by_rule_ids.append(a.id)
        except Exception:
            # On any error, do not broaden visibility beyond public/groups
            continue

    if allowed_by_rule_ids:
        allowed_q = allowed_q | Q(id__in=allowed_by_rule_ids)

    qs = qs.filter(allowed_q).distinct()

    # Sorting
    sort = request.GET.get("sort") or "-updated"
    sort_map = {
        "title": "title",
        "-title": "-title",
        "kind": "kind",
        "-kind": "-kind",
        "updated": "updated_at",
        "-updated": "-updated_at",
        "created": "created_at",
        "-created": "-created_at",
    }
    qs = qs.order_by(sort_map.get(sort, "-updated_at"))

    # ---- Collections + nesting ----
    # Build nested tree of collections and include only those with hits when filtered.
    all_collections = (
        Collection.objects.select_related("parent")
        .prefetch_related("tags", "allowed_groups")
        .order_by("parent__id", "sort_order", "title")
    )

    # Map assets to their collection
    assets_by_col: dict[int | None, list[Asset]] = {}
    for a in qs:
        assets_by_col.setdefault(a.collection_id, []).append(a)

    # Helper: detect whether any filter is applied (beyond defaults)
    def _any_filter_active(f: AssetFilterForm) -> bool:
        if not f.is_valid():
            return False
        cd = f.cleaned_data
        return any(
            [
                bool((cd.get("q") or "").strip()),
                bool(cd.get("kind")),
                bool(cd.get("visibility")),
                bool(cd.get("collection")),
                bool(cd.get("tags") and cd.get("tags").count() > 0),
                bool(cd.get("source")),
                bool(cd.get("referenced")),
            ]
        )

    filter_active = _any_filter_active(filter_form)

    # Build parent map and child lists
    by_id = {c.id: c for c in all_collections}
    parent_of = {c.id: (c.parent_id or None) for c in all_collections}
    children_of: dict[int | None, list[int]] = {}
    for c in all_collections:
        children_of.setdefault(c.parent_id, []).append(c.id)

    # Determine which collections to include: all if no filter; otherwise those
    # that have at least one matching asset OR are an ancestor of such a collection.
    include_ids: set[int] = set()
    if not filter_active:
        include_ids = set(by_id.keys())
    else:
        hit_cols = {col_id for col_id, items in assets_by_col.items() if col_id and items}
        include_ids.update(hit_cols)
        # add ancestors
        for cid in list(hit_cols):
            p = parent_of.get(cid)
            while p is not None and p not in include_ids:
                include_ids.add(p)
                p = parent_of.get(p)

    # Prune collections for non-superusers using two-tier logic:
    # - If a base collection rule (assets.collection.{id}) exists and is enabled,
    #   it fully controls visibility of that collection in the CMS tree.
    # - Otherwise, fall back to model visibility (public/internal/groups) OR
    #   explicit action/toolbar rules to include the node so users can reach controls.
    if not request.user.is_superuser:
        user_groups = _user_group_ids(request.user)

        def col_access(c: Collection) -> bool:
            vm = c.visibility_mode
            if vm == "public":
                return True
            if not request.user.is_authenticated:
                return False
            if vm == "internal":
                return True
            if vm == "groups":
                allowed = set(c.allowed_groups.values_list("id", flat=True))
                return bool(user_groups & allowed)
            return False

        def rule_allows_col(cid: int) -> bool:
            try:
                key_base = f"assets.collection.{cid}"
                act_key = f"cms.assets.collection.{cid}.actions"
                tool_key = f"cms.assets.collection.{cid}.toolbar"
                def allowed(key: str) -> bool:
                    return VisibilityRule.objects.filter(key=key, is_enabled=True).exists() and is_allowed(request.user, key)
                base_exists = VisibilityRule.objects.filter(key=key_base, is_enabled=True).exists()
                if base_exists:
                    # Base rule governs visibility entirely
                    return is_allowed(request.user, key_base)
                # No base rule: allow via model vis OR other related rules
                return col_access(by_id[cid]) or allowed(act_key) or allowed(tool_key)
            except Exception:
                return False

        include_ids = {
            cid for cid in include_ids
            if cid in by_id and rule_allows_col(cid)
        }

    # Build tree nodes
    def build_node(cid: int):
        c = by_id[cid]
        node = {
            "col": c,
            "assets": assets_by_col.get(c.id, []),
            "children": [],
        }
        for child_id in children_of.get(c.id, []):
            if child_id in include_ids:
                node["children"].append(build_node(child_id))
        return node

    roots = [cid for cid, pid in parent_of.items() if pid is None and cid in include_ids]
    tree = [build_node(cid) for cid in roots]

    # View mode
    view_mode = request.GET.get("view") or "grid"
    compact = request.GET.get("compact") == "1"

    # Forms (GET)
    if create_form is None:
        initial_asset = {}
        if filter_form.is_valid():
            selected_collection = filter_form.cleaned_data.get("collection")
            if selected_collection:
                initial_asset["collection"] = selected_collection
        initial_asset["appears_on"] = request.GET.get("appears_on") or ""
        create_form = AssetCreateForm(initial=initial_asset)

    if collection_form is None:
        initial_col = {}
        if filter_form.is_valid():
            selected_collection = filter_form.cleaned_data.get("collection")
            if selected_collection:
                initial_col["parent"] = selected_collection
        collection_form = CollectionForm(initial=initial_col)

    if tag_form is None:
        tag_form = TagForm()

    all_groups = Group.objects.all().order_by("name")

    ctx = {
        "form": filter_form,
        "create_form": create_form,
        "collection_form": collection_form,
        "tag_form": tag_form,
        "tree": tree,
        "all_collections": list(all_collections),
        "view_mode": view_mode,
        "compact": compact,
        "VISIBILITY_MODE_CHOICES": dict(VISIBILITY_MODE_CHOICES),
        "all_groups": all_groups,
    }
    return render(request, "assets/index.html", ctx)


# ---------- Asset inline ops --------------------------------------------------

@login_required
@require_POST
def asset_toggle_visibility(request, pk):
    a = get_object_or_404(Asset, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.asset.{a.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    a.visibility = "public" if a.effective_visibility in ("internal", "groups") else "internal"
    a.save()
    return JsonResponse({"ok": True, "visibility": a.effective_visibility})


@login_required
@require_POST
def asset_rename(request, pk):
    a = get_object_or_404(Asset, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.asset.{a.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)

    new_title = (request.POST.get("title") or "").strip()
    new_slug = (request.POST.get("slug") or "").strip()
    changed = False
    if new_title and new_title != a.title:
        a.title = new_title
        changed = True
    if new_slug and new_slug != a.slug:
        a.slug = new_slug
        changed = True
    if changed:
        a.save()
    return JsonResponse({"ok": True, "title": a.title, "slug": a.slug})


@login_required
def asset_data(request, pk):
    a = get_object_or_404(Asset.objects.select_related("collection").prefetch_related("tags"), pk=pk)
    if not _allowed_for(request.user, f"cms.assets.asset.{a.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    data = {
        "id": a.id,
        "title": a.title or "",
        "slug": a.slug or "",
        "visibility": a.visibility,
        "description": a.description or "",
        "collection": a.collection_id,
        "tags": list(a.tags.values_list("id", flat=True)),
        "url": a.url or "",
        "text_content": a.text_content or "",
        "has_file": bool(a.file),
        "file_url": (a.file.url if a.file else ""),
    }
    return JsonResponse({"ok": True, "asset": data})


@login_required
@require_POST
def asset_update(request, pk):
    a = get_object_or_404(Asset, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.asset.{a.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)

    a.title = (request.POST.get("title") or a.title).strip()
    slug = (request.POST.get("slug") or "").strip()
    if slug:
        a.slug = slug
    a.visibility = request.POST.get("visibility") or a.visibility
    a.description = request.POST.get("description") or ""

    col_id = request.POST.get("collection")
    if col_id:
        try:
            a.collection_id = int(col_id)
        except ValueError:
            pass

    tag_ids = request.POST.getlist("tags")
    if tag_ids:
        a.save()
        a.tags.set(Tag.objects.filter(id__in=tag_ids))

    new_file = request.FILES.get("file")
    new_url = (request.POST.get("url") or "").strip()
    new_text = (request.POST.get("text_content") or "").strip()
    provided = sum([1 if new_file else 0, 1 if new_url else 0, 1 if new_text else 0])
    if provided > 1:
        return JsonResponse({"ok": False, "error": "Provide at most one source (file OR url OR text)."}, status=400)
    if provided == 1:
        if new_file:
            a.file = new_file
            a.url = ""
            a.text_content = ""
        elif new_url:
            a.url = new_url
            a.file = None
            a.text_content = ""
        else:
            a.text_content = new_text
            a.file = None
            a.url = ""

    a.save()
    if request.headers.get("Hx-Request"):
        return JsonResponse({"ok": True})
    return HttpResponseRedirect(reverse("assets:index"))


@login_required
@require_POST
def asset_delete(request, pk):
    a = get_object_or_404(Asset, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.asset.{a.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    a.delete()
    return JsonResponse({"ok": True})


# ---------- Collection inline ops --------------------------------------------

@login_required
@require_POST
def collection_toggle_visibility(request, pk):
    c = get_object_or_404(Collection, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.collection.{c.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    c.visibility_mode = "public" if c.visibility_mode != "public" else "internal"
    c.save()
    return JsonResponse({"ok": True, "visibility": c.visibility_mode})


@login_required
@require_POST
def collection_rename(request, pk):
    c = get_object_or_404(Collection, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.collection.{c.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    new_title = (request.POST.get("title") or "").strip()
    new_slug = (request.POST.get("slug") or "").strip()
    changed = False
    if new_title and new_title != c.title:
        c.title = new_title
        changed = True
    if new_slug and new_slug != c.slug:
        c.slug = new_slug
        changed = True
    if changed:
        c.save()
    return JsonResponse({"ok": True, "title": c.title, "slug": c.slug})


@login_required
@require_POST
def collection_update(request, pk):
    c = get_object_or_404(Collection, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.collection.{c.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    form = CollectionForm(request.POST, instance=c)
    if form.is_valid():
        form.save()
        return JsonResponse({"ok": True})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@login_required
@require_POST
def collection_delete(request, pk):
    col = get_object_or_404(Collection, pk=pk)
    if not _allowed_for(request.user, f"cms.assets.collection.{col.id}.actions"):
        return JsonResponse({"ok": False, "error": "Not allowed"}, status=403)
    col.delete()
    return JsonResponse({"ok": True})


# ---------- PROTECTED FILE SERVING -------------------------------------------

def asset_file(request, pk):
    """
    Gate access to the actual file by visibility + user.
    Use ?dl=1 to force download (attachment); otherwise inline.
    """
    a = get_object_or_404(Asset.objects.select_related("collection"), pk=pk)

    if not a.file:
        raise Http404("No file on this asset.")

    if not _user_can_view_asset(request.user, a):
        # If not logged in, send to login page with return
        if not request.user.is_authenticated:
            login_url = settings.LOGIN_URL if hasattr(settings, "LOGIN_URL") else "/accounts/login/"
            next_url = request.get_full_path()
            return HttpResponseRedirect(f"{login_url}?next={next_url}")
        # Logged in but not allowed
        return HttpResponseForbidden("You do not have access to this file.")

    # Serve securely via Django (streaming); for production prefer X-Accel-Redirect / X-Sendfile
    mime, _ = mimetypes.guess_type(a.file.name)
    mime = mime or "application/octet-stream"
    fh = a.file.open("rb")
    resp = FileResponse(fh, content_type=mime)

    filename = os.path.basename(a.file.name)
    download = request.GET.get("dl") in ("1", "true", "yes", "download", "attachment")
    disp = "attachment" if download else "inline"
    resp["Content-Disposition"] = f'{disp}; filename="{filename}"'
    resp["Cache-Control"] = "private, max-age=0, no-cache, no-store"
    return resp
