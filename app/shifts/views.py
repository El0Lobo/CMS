"""Shift planning views."""

from __future__ import annotations

from datetime import timedelta
import json

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from app.events.models import Event
from app.shifts.forms import (
    EventShiftFormSet,
    ShiftAssignmentForm,
    ShiftStatsFilterForm,
    ShiftTemplateForm,
)
from app.shifts.models import Shift, ShiftAssignment, ShiftTemplate

User = get_user_model()


def _build_index_context(request):
    upcoming_shifts_qs = (
        Shift.objects.select_related("event", "template")
        .prefetch_related("assignments__user__profile")
        .filter(start_at__gte=timezone.now() - timedelta(days=7))
        .order_by("start_at")
    )
    upcoming_shifts = list(upcoming_shifts_qs)

    assignee_statuses = {
        ShiftAssignment.Status.ASSIGNED,
        ShiftAssignment.Status.COMPLETED,
    }
    for shift in upcoming_shifts:
        badges = []
        for assignment in shift.assignments.all():
            if assignment.status not in assignee_statuses:
                continue
            badges.append({
                'name': assignment.display_name,
                'user_id': assignment.user_id,
            })
        shift.assignment_badges = badges


    stats_form = ShiftStatsFilterForm(request.GET or None)
    stats_form.is_valid()
    since = stats_form.get_bounds()

    assignments = ShiftAssignment.objects.select_related("shift", "user")
    if since:
        assignments = assignments.filter(assigned_at__gte=since)

    stats_data = (
        assignments.values("user_id")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    user_ids = [row["user_id"] for row in stats_data if row["user_id"]]
    users = {u.id: u for u in User.objects.filter(id__in=user_ids).select_related("profile")}

    def _display_name(user):
        if not user:
            return '�'
        profile = getattr(user, 'profile', None)
        if profile:
            chosen = (getattr(profile, 'chosen_name', '') or '').strip()
            if chosen:
                return chosen
            legal = (getattr(profile, 'legal_name', '') or '').strip()
            if legal:
                return legal
        full_name = (getattr(user, 'get_full_name', lambda: '')() or '').strip()
        if full_name:
            return full_name
        username = getattr(user, 'get_username', lambda: str(getattr(user, 'pk', '')))()
        return username or str(getattr(user, 'pk', ''))

    stats = [
        {"user_id": row["user_id"], "total": row["total"], "display_name": _display_name(users.get(row["user_id"]))}
        for row in stats_data
    ]

    assign_form = ShiftAssignmentForm()
    assign_form.fields['user'].queryset = User.objects.all()  # or filter as needed
    template_form = ShiftTemplateForm()
    templates = ShiftTemplate.objects.order_by("order", "name")

    taken_shift_ids = set()
    if request.user.is_authenticated:
        taken_shift_ids = set(
            ShiftAssignment.objects.filter(
                user=request.user,
                status__in=[
                    ShiftAssignment.Status.ASSIGNED,
                    ShiftAssignment.Status.COMPLETED,
                ],
                shift__in=upcoming_shifts,
            ).values_list("shift_id", flat=True)
        )

    template_edit_forms = {
        tmpl.id: ShiftTemplateForm(instance=tmpl, prefix=f"tmpl-{tmpl.id}")
        for tmpl in templates
    }
    template_forms = [(tmpl, template_edit_forms[tmpl.id]) for tmpl in templates]

    event_ids = {shift.event_id for shift in upcoming_shifts}
    event_map = {
        event.id: event
        for event in Event.objects.filter(pk__in=event_ids)
        .select_related("created_by", "updated_by")
        .prefetch_related("categories", "performers__band")
    }

    events_by_id = {}
    events_with_shifts = []
    for shift in upcoming_shifts:
        event = event_map.get(shift.event_id, shift.event)
        entry = events_by_id.get(event.id)
        if not entry:
            entry = {"event": event, "shifts": []}
            events_by_id[event.id] = entry
            events_with_shifts.append(entry)
        entry["shifts"].append(shift)

    for entry in events_with_shifts:
        options = []
        for s in entry["shifts"]:
            try:
                start_label = timezone.localtime(s.start_at).strftime('%H:%M')
                end_label = timezone.localtime(s.end_at).strftime('%H:%M')
            except Exception:
                start_label = s.start_at.strftime('%H:%M') if hasattr(s.start_at, 'strftime') else ''
                end_label = s.end_at.strftime('%H:%M') if hasattr(s.end_at, 'strftime') else ''
            if start_label and end_label:
                label = f"{s.title} ({start_label}-{end_label})"
            else:
                label = s.title
            options.append({'id': s.id, 'label': label, 'title': s.title})
    entry['assign_options_json'] = json.dumps(options)
    entry['has_shift_options'] = bool(options)


    return {
        "shifts": upcoming_shifts,
        "events_with_shifts": events_with_shifts,
        "assign_form": assign_form,
        "stats_form": stats_form,
        "stats": stats,
        "taken_shift_ids": taken_shift_ids,
        "template_form": template_form,
        "templates": templates,
        "template_edit_forms": template_edit_forms,
        "template_forms": template_forms,
    }


@login_required
def index(request: HttpRequest) -> HttpResponse:
    context = _build_index_context(request)
    return render(request, "shifts/index.html", context)
@login_required
def assign(request: HttpRequest, shift_id: int) -> HttpResponse:
    if not request.user.is_superuser:
        messages.error(request, "Only administrators can assign other users to shifts.")
        return redirect("shifts:index")

    shift = get_object_or_404(Shift, pk=shift_id)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    form = ShiftAssignmentForm(request.POST)
    if form.is_valid():
        user = form.cleaned_data.get("user")
        notes = form.cleaned_data.get("notes") or ""

        if not user:
            ShiftAssignment.objects.filter(shift=shift).delete()
            message_text = "Assignment cleared."
        else:
            assignment, _ = ShiftAssignment.objects.get_or_create(
                shift=shift,
                user=user,
                defaults={
                    "status": ShiftAssignment.Status.ASSIGNED,
                    "notes": notes,
                    "assigned_by": request.user,
                },
            )
            assignment.status = ShiftAssignment.Status.ASSIGNED
            assignment.notes = notes
            assignment.assigned_by = request.user
            assignment.save()
            message_text = "Assignment updated."

        messages.success(request, message_text)
        if request.htmx:
            response = HttpResponse(status=204)
            response["Hx-Trigger"] = "shift:assignment"
            response["Hx-Redirect"] = reverse("shifts:index")
            return response
        return redirect("shifts:index")

    return render(
        request,
        "shifts/partials/assignment_form_body.html",
        {"assign_form": form, "shift": shift},
        status=400,
    )


@login_required
def create_template(request: HttpRequest) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    form = ShiftTemplateForm(request.POST)
    if form.is_valid():
        form.save()
        messages.success(request, "Standard shift saved.")
        if request.htmx:
            response = HttpResponse(status=204)
            response["Hx-Redirect"] = reverse("shifts:index")
            return response
        return redirect("shifts:index")

    return render(
        request,
        "shifts/partials/template_form_body.html",
        {"template_form": form},
        status=400,
    )


@login_required
def update_template(request: HttpRequest, pk: int) -> HttpResponse:
    template = get_object_or_404(ShiftTemplate, pk=pk)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    form = ShiftTemplateForm(request.POST, instance=template, prefix=f"tmpl-{pk}")
    if form.is_valid():
        form.save()
        messages.success(request, "Standard shift updated.")
        return redirect("shifts:index")

    messages.error(request, "Please correct the errors below.")
    context = _build_index_context(request)
    context["template_edit_forms"][pk] = form
    context["template_forms"] = [
        (tmpl, context["template_edit_forms"][tmpl.id]) for tmpl in context["templates"]
    ]
    return render(request, "shifts/index.html", context, status=400)


@login_required
def delete_template(request: HttpRequest, pk: int) -> HttpResponse:
    template = get_object_or_404(ShiftTemplate, pk=pk)
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    template.delete()
    messages.success(request, "Standard shift deleted.")
    return redirect("shifts:index")


@login_required
def take(request: HttpRequest, shift_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseBadRequest("POST required")

    shift = get_object_or_404(Shift, pk=shift_id)

    if not shift.allow_signup:
        messages.error(request, "This shift is not open for self sign-up.")
        return redirect("shifts:index")

    if shift.is_full and not shift.is_taken_by(request.user):
        messages.error(request, "This shift is already filled.")
        return redirect("shifts:index")

    assignment, _ = ShiftAssignment.objects.get_or_create(
        shift=shift,
        user=request.user,
        defaults={
            "status": ShiftAssignment.Status.ASSIGNED,
            "assigned_by": request.user,
        },
    )

    assignment.status = ShiftAssignment.Status.ASSIGNED
    assignment.assigned_by = request.user
    assignment.save()

    messages.success(request, "You have been assigned to this shift.")
    return redirect("shifts:index")


@login_required
def manage_event(request: HttpRequest, event_slug: str) -> HttpResponse:
    event = get_object_or_404(Event, slug=event_slug)
    if request.method == "POST":
        formset = EventShiftFormSet(request.POST, instance=event)
        if formset.is_valid():
            instances = formset.save(commit=False)
            for inst in instances:
                inst.updated_by = request.user
                if not inst.pk:
                    inst.created_by = request.user
                inst.save()
            for obj in formset.deleted_objects:
                obj.delete()
            messages.success(request, "Shifts updated.")
            return redirect("shifts:manage_event", event_slug=event.slug)
    else:
        formset = EventShiftFormSet(instance=event)
    return render(
        request,
        "shifts/manage_event.html",
        {"event": event, "formset": formset},
    )
