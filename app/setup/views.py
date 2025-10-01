from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.apps import apps
from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import render_to_string
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.db.models.functions.text import StrIndex
from django.db.models import F, Value, Case, When, CharField, Q
from django.db.models.functions import Substr
from .models import SiteSettings, OpeningHour, VisibilityRule
from .forms import SettingsForm, TierFormSet, HourFormSet, GroupFormSet, VisibilityRuleForm


def superuser_required(u):
    return u.is_superuser


def ensure_hours_for(settings_obj):
    """Make sure all 7 weekday rows exist for this settings singleton."""
    existing = set(settings_obj.hours.values_list("weekday", flat=True))
    for wd in range(7):
        if wd not in existing:
            OpeningHour.objects.create(settings=settings_obj, weekday=wd, closed=True)


@login_required
@user_passes_test(superuser_required)
@transaction.atomic
def setup_view(request):
    """
    CMS Setup: edits SiteSettings + inline formsets, and controls which public pages appear.

    - Checkbox order on this page determines nav order (saved as newline-separated text).
    - Contact is automatically moved to the end when saving.
    """
    settings_obj = SiteSettings.get_solo()
    ensure_hours_for(settings_obj)

    # Mode-specific public pages (display order for the checkboxes)
    mode = (settings_obj.mode or "VENUE").upper()
    PAGES_BY_MODE = {
        # includes Shows/Music/Videos/Store so they can be selected when useful
        "VENUE":  ["Home", "Events", "Menu", "Gallery", "Blog", "About", "Shows", "Music", "Videos", "Store", "Contact"],
        "BAND":   ["Home", "Shows", "Music", "Videos", "Blog", "About", "Store", "Contact"],
        "PERSON": ["Home", "Posts", "About", "Contact"],
    }
    available_pages = PAGES_BY_MODE.get(mode, PAGES_BY_MODE["VENUE"])

    if request.method == "POST":
        form = SettingsForm(request.POST, request.FILES, instance=settings_obj)
        tiers = TierFormSet(request.POST, instance=settings_obj, prefix="tiers")
        hours = HourFormSet(request.POST, instance=settings_obj, prefix="hours")
        roles = GroupFormSet(request.POST, queryset=Group.objects.all().order_by("name"), prefix="roles")

        # Partial-save: save what validates, warn on the rest
        main_ok = form.is_valid()
        tiers_ok = tiers.is_valid()
        hours_ok = hours.is_valid()
        roles_ok = roles.is_valid()

        if main_ok:
            settings_saved = form.save()

            # If nothing selected, auto-populate with all for the current mode
            if not (settings_saved.required_pages or "").strip():
                settings_saved.required_pages = "\n".join(available_pages)
                settings_saved.save(update_fields=["required_pages"])

            skipped = []

            if tiers_ok:
                tiers.save()
            else:
                skipped.append("Membership tiers")

            if hours_ok:
                hours.save()
            else:
                skipped.append("Opening times")

            if roles_ok:
                roles.save()
            else:
                skipped.append("Roles")

            # Auto-create public pages (if a Page model exists)
            created_pages = []
            try:
                Page = apps.get_model("app.pages", "Page")
            except Exception:
                Page = None

            titles = [t.strip() for t in (settings_saved.required_pages or "").splitlines() if t.strip()]
            if Page:
                for title in titles:
                    slug = title.lower().strip().replace(" ", "-")
                    obj, created = Page.objects.get_or_create(slug=slug, defaults={"title": title})
                    if created:
                        created_pages.append(title)

            msg = "Settings saved."
            if created_pages:
                msg += " Created pages: " + ", ".join(created_pages) + "."
            messages.success(request, msg)

            if skipped:
                messages.warning(request, "Some sections were not saved: " + ", ".join(skipped) + ".")

            return redirect("setup:setup")
        else:
            # With our permissive form, this should be rare; still show what failed
            messages.error(request, "Could not save the core settings. Please review the highlighted fields.")
    else:
        form = SettingsForm(instance=settings_obj)
        tiers = TierFormSet(instance=settings_obj, prefix="tiers")
        hours = HourFormSet(instance=settings_obj, prefix="hours")
        roles = GroupFormSet(queryset=Group.objects.all().order_by("name"), prefix="roles")

    # Build selected list from stored newline-separated text (used by template for checked state)
    selected_pages = [t.strip() for t in (form.instance.required_pages or "").splitlines() if t.strip()]

    current_mode = (form.instance.mode or "VENUE").lower()
    return render(request, "setup/setup.html", {
        "form": form,
        "tiers": tiers,
        "hours": hours,
        "roles": roles,
        "available_pages": available_pages,
        "selected_pages": selected_pages,   # used in template to mark checkboxes
        "current_mode": current_mode,
    })


@login_required
@user_passes_test(superuser_required)
def visibility_list(request):
    q = request.GET.get("q", "").strip()
    sort = request.GET.get("sort", "key")
    direction = request.GET.get("dir", "asc")

    rules = VisibilityRule.objects.all()

    if q:
        rules = rules.filter(
            Q(key__icontains=q) |
            Q(label__icontains=q) |
            Q(notes__icontains=q)
        )

    rules = rules.annotate(first_dot=StrIndex(F("key"), Value(".")))
    rules = rules.annotate(after_first=Substr(F("key"), F("first_dot") + 1))
    rules = rules.annotate(second_rel=StrIndex(F("after_first"), Value(".")))
    rules = rules.annotate(
        group_name=Case(
            When(second_rel__gt=1,
                 then=Substr(F("key"), F("first_dot") + 1, F("second_rel") - 1)),
            default=Value(""),
            output_field=CharField(),
        )
    )

    allowed_sorts = {"key", "label", "is_enabled", "notes", "group"}  # add "group"

    if sort not in allowed_sorts:
        sort = "key"

    # map "group" to the annotation name "group_name"
    sort_field = "group_name" if sort == "group" else sort
    sort_expr = f"-{sort_field}" if direction == "desc" else sort_field

    rules = rules.order_by(sort_expr, "key")  # stable tiebreak

    ctx = {"rules": rules, "q": q, "sort": sort, "direction": direction}

    if request.headers.get("HX-Request") == "true":
        return render(request, "setup/_visibility_table.html", ctx)

    return render(request, "setup/visibility_list.html", ctx)
@login_required
@user_passes_test(superuser_required)
def visibility_edit(request):
    key = request.GET.get("key", "")
    label = request.GET.get("label", "")
    instance = VisibilityRule.objects.filter(key=key).first()
    if request.method == "POST":
        form = VisibilityRuleForm(request.POST, instance=instance)
        if form.is_valid():
            form.save()
            messages.success(request, "Visibility saved.")
            return redirect("setup:visibility_list")
    else:
        form = VisibilityRuleForm(instance=instance) if instance else VisibilityRuleForm(initial={"key": key, "label": label})
    return render(request, "setup/visibility_edit.html", {"form": form})


@login_required
@user_passes_test(superuser_required)
def visibility_delete(request, rule_id):
    rule = get_object_or_404(VisibilityRule, id=rule_id)
    rule.delete()
    messages.success(request, "Visibility rule deleted.")
    return redirect("setup:visibility_list")


@login_required
@user_passes_test(superuser_required)
@require_http_methods(["GET", "POST"])
def visibility_picker(request):
    """
    HTMX popover with role checkboxes for a visibility key.
    - GET: render the popover
    - POST: update allowed_groups, re-render (with 'saved' tick)
    """
    key = (request.GET.get("key") or request.POST.get("key") or "").strip()
    label = (request.GET.get("label") or request.POST.get("label") or "").strip()
    if not key:
        return HttpResponseBadRequest("Missing key")

    rule, _ = VisibilityRule.objects.get_or_create(key=key, defaults={"label": label or key})
    all_groups = Group.objects.all().order_by("name")

    if request.method == "POST":
        selected = request.POST.getlist("groups")
        rule.allowed_groups.set(Group.objects.filter(id__in=selected))
        rule.is_enabled = True
        rule.save()
        saved = True
    else:
        saved = False

    html = render_to_string("setup/visibility_picker.html", {
        "rule": rule,
        "all_groups": all_groups,
        "saved": saved,
        "label": rule.label or label or key,
        "key": key,
    }, request=request)
    return HttpResponse(html)
